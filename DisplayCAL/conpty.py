# -*- coding: utf-8 -*-
# DisplayCAL/conpty.py
"""
Windows ConPTY backend implementation for wexpect-like functionality.
Requires Windows 10 (1809) or later.

This module provides a modern, reliable way to interact with console applications
on Windows using the Pseudo Console (ConPTY) API introduced in Windows 10 October
2018 Update (version 1809, build 17763).

Key advantages over the legacy screen-scraping approach:
- Reliable Unicode handling (no console codepage limitations)
- True pseudoconsole functionality
- Improved stability and performance
"""

import ctypes
from ctypes import wintypes
import os
import queue
import subprocess
import sys
import threading
import time
import traceback
import winerror # For error codes like ERROR_BROKEN_PIPE
import re # Needed for expect methods

# Import base classes/helpers from the main wexpect module
try:
    # Assuming wexpect.py is in the same package directory
    from .wexpect import EOF, TIMEOUT, ExceptionPexpect, searcher_re, searcher_string, log, which, split_command_line
except ImportError as e:
    # Fallback for potential standalone testing or different structure
    print(f"Warning: Could not import base classes from .wexpect: {e}. Define placeholders.")
    class ExceptionPexpect(Exception): pass
    class EOF(ExceptionPexpect): pass
    class TIMEOUT(ExceptionPexpect): pass
    # Define dummy searchers if needed for basic functionality without full expect
    class searcher_re:
        def search(self, *args): return -1
    class searcher_string:
        def search(self, *args): return -1
    def log(*args, **kwargs): print("LOG:", *args) # Simple log placeholder
    # Import shutil for which fallback
    import shutil
    def which(cmd): return shutil.which(cmd)
    def split_command_line(cmd): return subprocess.list2cmdline([cmd]) # Simplistic

# --- Win32 Definitions ---
# The following defines Windows API types, constants, and function prototypes
# using ctypes to interface directly with the Windows API.
BOOL = wintypes.BOOL
DWORD = wintypes.DWORD
HANDLE = wintypes.HANDLE
LPVOID = wintypes.LPVOID
PVOID = ctypes.c_void_p
LPCWSTR = wintypes.LPCWSTR
LPWSTR = wintypes.LPWSTR
WORD = wintypes.WORD
ULONG_PTR = wintypes.WPARAM
SIZE_T = ctypes.c_size_t
PSIZE_T = ctypes.POINTER(SIZE_T)
HRESULT = wintypes.HRESULT
INVALID_HANDLE_VALUE = -1
STILL_ACTIVE = 259
ERROR_BROKEN_PIPE = 109
INFINITE = 0xFFFFFFFF

class COORD(ctypes.Structure):
    """Windows COORD structure - defines a character cell coordinate (X,Y)."""
    _fields_ = [("X", wintypes.SHORT), ("Y", wintypes.SHORT)]

class SECURITY_ATTRIBUTES(ctypes.Structure):
    """Windows SECURITY_ATTRIBUTES structure - used for handle inheritance."""
    _fields_ = [("nLength", DWORD), ("lpSecurityDescriptor", LPVOID), ("bInheritHandle", BOOL)]
LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)

class PROCESS_INFORMATION(ctypes.Structure):
    """Windows PROCESS_INFORMATION structure - holds info about a newly created process."""
    _fields_ = [("hProcess", HANDLE), ("hThread", HANDLE), ("dwProcessId", DWORD), ("dwThreadId", DWORD)]
LPPROCESS_INFORMATION = ctypes.POINTER(PROCESS_INFORMATION)

# Re-import STARTUPINFO here, maybe from ctypes.wintypes if available and sufficient,
# otherwise define it or import from win32process (needs pywin32 dependency for this file too)
try:
    # Try importing STARTUPINFO from win32process first
    from win32process import STARTUPINFO, GetStartupInfo
except ImportError:
    # Basic definition if pywin32 not available here
    class STARTUPINFO(ctypes.Structure):
        """Windows STARTUPINFO structure - used for process creation settings."""
        _fields_ = [("cb", DWORD), ("lpReserved", LPWSTR), ("lpDesktop", LPWSTR),
                    ("lpTitle", LPWSTR), ("dwX", DWORD), ("dwY", DWORD),
                    ("dwXSize", DWORD), ("dwYSize", DWORD), ("dwXCountChars", DWORD),
                    ("dwYCountChars", DWORD), ("dwFillAttribute", DWORD), ("dwFlags", DWORD),
                    ("wShowWindow", WORD), ("cbReserved2", WORD), ("lpReserved2", PVOID), # Use PVOID
                    ("hStdInput", HANDLE), ("hStdOutput", HANDLE), ("hStdError", HANDLE)]
    def GetStartupInfo(): # Dummy GetStartupInfo if pywin32 missing
        si = STARTUPINFO()
        si.cb = ctypes.sizeof(STARTUPINFO)
        return si

class STARTUPINFOEXW(ctypes.Structure):
    """Windows STARTUPINFOEXW structure - extended STARTUPINFO with attribute list."""
    _fields_ = [("StartupInfo", STARTUPINFO), ("lpAttributeList", PVOID)] # Use PVOID
LPSTARTUPINFOEXW = ctypes.POINTER(STARTUPINFOEXW)

# ConPTY and process creation flags
PROC_THREAD_ATTRIBUTE_PSEUDOCONSOLE = 0x00020016  # Attribute for pseudo console
EXTENDED_STARTUPINFO_PRESENT = 0x00080000         # Process creation flag for extended startup info
CREATE_UNICODE_ENVIRONMENT = 0x00000400           # Process creation flag for Unicode environment

# Load and configure Windows API functions from kernel32.dll
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
CreatePipe = kernel32.CreatePipe; CreatePipe.argtypes = [ctypes.POINTER(HANDLE), ctypes.POINTER(HANDLE), LPSECURITY_ATTRIBUTES, DWORD]; CreatePipe.restype = BOOL
CloseHandle = kernel32.CloseHandle; CloseHandle.argtypes = [HANDLE]; CloseHandle.restype = BOOL
CreateProcessW = kernel32.CreateProcessW; CreateProcessW.argtypes = [LPCWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, LPCWSTR, LPSTARTUPINFOEXW, LPPROCESS_INFORMATION]; CreateProcessW.restype = BOOL
InitializeProcThreadAttributeList = kernel32.InitializeProcThreadAttributeList; InitializeProcThreadAttributeList.argtypes = [PVOID, DWORD, DWORD, ctypes.POINTER(SIZE_T)]; InitializeProcThreadAttributeList.restype = BOOL # Use PVOID
UpdateProcThreadAttribute = kernel32.UpdateProcThreadAttribute; UpdateProcThreadAttribute.argtypes = [PVOID, DWORD, ULONG_PTR, PVOID, SIZE_T, PVOID, PSIZE_T]; UpdateProcThreadAttribute.restype = BOOL # Use PVOID
DeleteProcThreadAttributeList = kernel32.DeleteProcThreadAttributeList; DeleteProcThreadAttributeList.argtypes = [PVOID]; DeleteProcThreadAttributeList.restype = None # Use PVOID
GetExitCodeProcess = kernel32.GetExitCodeProcess; GetExitCodeProcess.argtypes = [HANDLE, ctypes.POINTER(DWORD)]; GetExitCodeProcess.restype = BOOL
TerminateProcess = kernel32.TerminateProcess; TerminateProcess.argtypes = [HANDLE, wintypes.UINT]; TerminateProcess.restype = BOOL
ReadFile = kernel32.ReadFile; ReadFile.argtypes = [HANDLE, PVOID, DWORD, ctypes.POINTER(DWORD), LPVOID]; ReadFile.restype = BOOL # Use PVOID
WriteFile = kernel32.WriteFile; WriteFile.argtypes = [HANDLE, PVOID, DWORD, ctypes.POINTER(DWORD), LPVOID]; WriteFile.restype = BOOL # Use PVOID
WaitForSingleObject = kernel32.WaitForSingleObject; WaitForSingleObject.argtypes = [HANDLE, DWORD]; WaitForSingleObject.restype = DWORD
GetLastError = kernel32.GetLastError; GetLastError.restype = DWORD

# Try loading the ConPTY-specific APIs (only available on Windows 10 1809+)
try:
    # ConPTY API functions
    CreatePseudoConsole = kernel32.CreatePseudoConsole; CreatePseudoConsole.argtypes = [COORD, HANDLE, HANDLE, DWORD, ctypes.POINTER(HANDLE)]; CreatePseudoConsole.restype = HRESULT
    ResizePseudoConsole = kernel32.ResizePseudoConsole; ResizePseudoConsole.argtypes = [HANDLE, COORD]; ResizePseudoConsole.restype = HRESULT
    ClosePseudoConsole = kernel32.ClosePseudoConsole; ClosePseudoConsole.argtypes = [HANDLE]; ClosePseudoConsole.restype = None
    _CONPTY_AVAILABLE = True
except AttributeError:
    # ConPTY APIs not available on this Windows version
    _CONPTY_AVAILABLE = False

S_OK = 0
def SUCCEEDED(hr): return hr >= 0
# --- End Win32 Definitions ---

class spawn_windows_conpty(object):
    """
    Windows spawn implementation using the ConPTY API (Requires Windows 10 1809+).
    Provides a pexpect-like interface for interacting with console applications.
    
    This implementation uses the modern Windows Pseudo Console API to create a
    true pseudoterminal, allowing for reliable and proper handling of console
    applications, including those that use complex console features and Unicode text.
    
    Threading model:
    - A reader thread continually reads from the ConPTY output pipe
    - A monitor thread watches for process termination
    - Thread-safe communication via queues and protection with locks
    
    Encoding handling:
    - Properly handles Unicode via the specified encoding parameters
    - Falls back to a secondary encoding if needed for non-decodable bytes
    """
    def __init__(
        self,
        command,
        args=None,
        timeout=30,
        maxread=4096,
        searchwindowsize=None,
        logfile=None,
        cwd=None,
        env=None,
        encoding='utf-8',
        errors='replace',
        fallback_encoding='latin-1',
        dimensions=(80, 25)
    ):
        if not _CONPTY_AVAILABLE:
            raise OSError("ConPTY API is not available on this system.")
        if args is None: args = []
        self.stdin = sys.stdin; self.stdout = sys.stdout; self.stderr = sys.stderr
        self.searcher = None; self.ignorecase = False
        self.before = None; self.after = None; self.match = None; self.match_index = None
        self.terminated = True; self.exitstatus = None; self.signalstatus = None; self.status = None
        self.flag_eof = False; self.pid = None; self.child_fd = -1
        self.timeout = timeout; self.delimiter = EOF
        self.logfile = logfile; self.logfile_read = None; self.logfile_send = None
        self.maxread = maxread; self.buffer = ""; self.searchwindowsize = searchwindowsize
        self.delaybeforesend = 0.05; self.delayafterclose = 0.1; self.delayafterterminate = 0.1
        self.softspace = False; self.name = f"<{repr(self)}>"
        self.encoding = encoding; self.errors = errors; self.fallback_encoding = fallback_encoding
        self.closed = True; self.cwd = cwd; self.env = env; self.dimensions = dimensions

        # Process and ConPTY handles
        self._proc_info = PROCESS_INFORMATION()
        self._conpty_handle = HANDLE(INVALID_HANDLE_VALUE)
        self._pty_in = HANDLE(INVALID_HANDLE_VALUE)    # Our connection to the ConPTY input
        self._pty_out = HANDLE(INVALID_HANDLE_VALUE)   # Our connection to the ConPTY output
        self._child_stdin = HANDLE(INVALID_HANDLE_VALUE)  # Child's stdin (write side of pipe)
        self._child_stdout = HANDLE(INVALID_HANDLE_VALUE) # Child's stdout (read side of pipe)
        self._proc_info.hProcess = HANDLE(INVALID_HANDLE_VALUE)
        self._proc_info.hThread = HANDLE(INVALID_HANDLE_VALUE)

        # Thread synchronization
        self._reader_thread = None  # Thread that reads from the ConPTY
        self._read_queue = queue.Queue()  # Queue for passing data from reader thread to main thread
        self._process_ended_event = threading.Event()  # Signals when the child process has terminated
        self._monitor_thread = None  # Thread that monitors if the child process is alive
        self._state_lock = threading.Lock()  # Protects state that's accessed by multiple threads

        # Prepare command/args
        if not isinstance(args, list): raise TypeError("args must be a list.")
        if not args:
            try: self.args = split_command_line(command); self.command = self.args[0]
            except Exception as e: raise ExceptionPexpect(f"Parse error: {command}\n{e}")
        else:
            self.args = args[:]; self.args.insert(0, command); self.command = command
        command_with_path = which(self.command)
        if command_with_path is None: raise ExceptionPexpect(f"Command not found: {self.command}.")
        self.command = command_with_path; self.args[0] = self.command
        try: self.command_line = subprocess.list2cmdline(self.args)
        except Exception as e: raise ExceptionPexpect(f"Cmdline format error: {e}")
        self.name = f"<{self.command_line}>"

        # Spawn
        try: self._spawn()
        except Exception: self._cleanup_handles(); raise

    def _spawn(self):
        """
        Creates the ConPTY and child process.
        
        This method:
        1. Creates pipes to communicate with the ConPTY
        2. Creates the ConPTY itself using Windows API
        3. Sets up process attributes to connect to the ConPTY
        4. Spawns the child process connected to the ConPTY
        5. Launches reader and monitor threads
        """
        # 1. Create pipes
        sec_attrs = SECURITY_ATTRIBUTES(ctypes.sizeof(SECURITY_ATTRIBUTES), None, False)
        h_pty_in_read, h_pty_in_write = HANDLE(), HANDLE()
        h_pty_out_read, h_pty_out_write = HANDLE(), HANDLE()
        if not CreatePipe(ctypes.byref(h_pty_in_read), ctypes.byref(h_pty_in_write), ctypes.byref(sec_attrs), 0):
            raise ctypes.WinError(GetLastError())
        self._pty_in = h_pty_in_read; self._child_stdin = h_pty_in_write
        if not CreatePipe(ctypes.byref(h_pty_out_read), ctypes.byref(h_pty_out_write), ctypes.byref(sec_attrs), 0):
            CloseHandle(h_pty_in_read); CloseHandle(h_pty_in_write)
            raise ctypes.WinError(GetLastError())
        self._pty_out = h_pty_out_write; self._child_stdout = h_pty_out_read

        # 2. Create ConPTY
        conpty_size = COORD(self.dimensions[0], self.dimensions[1])
        hr = CreatePseudoConsole(conpty_size, self._pty_in, self._pty_out, 0, ctypes.byref(self._conpty_handle))
        if not SUCCEEDED(hr): self._cleanup_handles(); raise ExceptionPexpect(f"CreatePseudoConsole failed: {hr:#010x}")

        # 3. Prepare Startup Info
        startup_info_ex = STARTUPINFOEXW()
        startup_info_ex.StartupInfo.cb = ctypes.sizeof(STARTUPINFOEXW)
        size = SIZE_T(0)
        # First, get the size needed for the attribute list
        InitializeProcThreadAttributeList(None, 1, 0, ctypes.byref(size))
        if size.value == 0: self._cleanup_handles(); raise ExceptionPexpect("AttrList size=0")
        # Allocate the attribute list buffer of required size
        startup_info_ex.lpAttributeList = ctypes.create_string_buffer(size.value)
        if not InitializeProcThreadAttributeList(startup_info_ex.lpAttributeList, 1, 0, ctypes.byref(size)):
            self._cleanup_handles(); raise ctypes.WinError(GetLastError())
        # Set the ConPTY handle as the pseudo console attribute
        hpcon_value = self._conpty_handle.value
        attr_value_ptr = ctypes.cast(ctypes.byref(HANDLE(hpcon_value)), PVOID)
        if not UpdateProcThreadAttribute(startup_info_ex.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_PSEUDOCONSOLE,
                                         attr_value_ptr, ctypes.sizeof(HANDLE), None, None):
            self._cleanup_handles(); raise ctypes.WinError(GetLastError())

        # 4. Prepare Environment
        env_block = None
        if self.env is not None:
            # Create a Unicode environment block from the env dict
            effective_env = os.environ.copy(); effective_env.update({k: str(v) for k, v in self.env.items()})
            env_strings = "".join(f"{k}={v}\0" for k, v in effective_env.items()) + "\0"
            env_block = env_strings.encode('utf-16le')  # Windows environment blocks use UTF-16LE

        # 5. Create Process
        creation_flags = EXTENDED_STARTUPINFO_PRESENT | CREATE_UNICODE_ENVIRONMENT
        proc_attrs = SECURITY_ATTRIBUTES(ctypes.sizeof(SECURITY_ATTRIBUTES), None, False)
        thread_attrs = SECURITY_ATTRIBUTES(ctypes.sizeof(SECURITY_ATTRIBUTES), None, False)

        success = CreateProcessW(None, LPWSTR(self.command_line), ctypes.byref(proc_attrs), ctypes.byref(thread_attrs),
                                 False, creation_flags, env_block, LPCWSTR(self.cwd) if self.cwd else None,
                                 ctypes.byref(startup_info_ex), ctypes.byref(self._proc_info))

        # Clean up attribute list after process creation
        if startup_info_ex.lpAttributeList: DeleteProcThreadAttributeList(startup_info_ex.lpAttributeList)
        if not success: self._cleanup_handles(); raise ctypes.WinError(GetLastError())

        # 6. Close parent-side ConPTY handles
        # Now that the ConPTY is connected to the process, we don't need our endpoints
        if self._pty_in.value != INVALID_HANDLE_VALUE: CloseHandle(self._pty_in); self._pty_in = HANDLE(INVALID_HANDLE_VALUE)
        if self._pty_out.value != INVALID_HANDLE_VALUE: CloseHandle(self._pty_out); self._pty_out = HANDLE(INVALID_HANDLE_VALUE)

        # 7. Update state and start threads
        self.pid = self._proc_info.dwProcessId
        self.terminated = False; self.closed = False
        self._process_ended_event.clear()
        
        # Start reader thread - continuously reads from the ConPTY output
        self._reader_thread = threading.Thread(target=self._read_loop, daemon=True, name=f"ConPTYReader-{self.pid}")
        self._reader_thread.start()
        
        # Start monitor thread - watches for process termination
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True, name=f"ConPTYMonitor-{self.pid}")
        self._monitor_thread.start()

    def _cleanup_handles(self):
        """
        Safely close all handles and reset state.
        
        This method is called when:
        1. The spawn method fails during setup
        2. The process is being terminated
        3. The instance is being deleted
        
        It ensures that all Windows handles are properly closed to prevent resource leaks.
        """
        # log("ConPTY: Cleaning up handles.") # Optional
        with self._state_lock:
            handles_to_close = [
                (self._child_stdin, "_child_stdin"), (self._child_stdout, "_child_stdout"),
                (self._pty_in, "_pty_in"), (self._pty_out, "_pty_out"),
                (self._proc_info.hThread, "proc_thread"), (self._proc_info.hProcess, "proc_process")
            ]
            # Close ConPTY handle first if still valid
            if self._conpty_handle.value != INVALID_HANDLE_VALUE:
                if ClosePseudoConsole:
                    try: ClosePseudoConsole(self._conpty_handle)
                    except Exception: pass
                self._conpty_handle = HANDLE(INVALID_HANDLE_VALUE)

            for handle, name in handles_to_close:
                if handle.value != INVALID_HANDLE_VALUE:
                    try: CloseHandle(handle)
                    except Exception: pass
                    # Reset handle variable
                    setattr(self, name if name.startswith('_') else f"_{name}", HANDLE(INVALID_HANDLE_VALUE))

            # Ensure ProcessInfo handles are reset outside loop if needed
            if self._proc_info.hThread.value != INVALID_HANDLE_VALUE: self._proc_info.hThread = HANDLE(INVALID_HANDLE_VALUE)
            if self._proc_info.hProcess.value != INVALID_HANDLE_VALUE: self._proc_info.hProcess = HANDLE(INVALID_HANDLE_VALUE)
            # self._proc_info = PROCESS_INFORMATION() # Re-initializing might discard PID? Reset handles instead.

    def _read_loop(self):
        """
        Reader thread function that continuously reads from the child process output.
        
        This runs in a separate thread to allow asynchronous reading from the ConPTY.
        It reads raw bytes from the pipe, decodes them using the specified encoding,
        and places decoded strings in the queue for the main thread to consume.
        
        If encoding errors occur, it attempts to use the fallback_encoding.
        Thread-safety is maintained using the _state_lock when accessing shared state.
        """
        # log("ConPTY: Reader thread started") # Optional
        try:
            buffer_size = self.maxread
            read_buffer = ctypes.create_string_buffer(buffer_size)
            bytes_read = DWORD(0)
            while True:
                handle_value = INVALID_HANDLE_VALUE
                with self._state_lock:
                    if self.closed or self._child_stdout.value == INVALID_HANDLE_VALUE: break
                    handle_value = self._child_stdout.value # Get handle value under lock
                if handle_value == INVALID_HANDLE_VALUE: break

                stdout_handle = HANDLE(handle_value) # Use the value safely outside lock
                success = ReadFile(stdout_handle, read_buffer, buffer_size, ctypes.byref(bytes_read), None)
                last_error = GetLastError()

                if not success:
                    if last_error == ERROR_BROKEN_PIPE: break  # Pipe closed normally
                    else: self._read_queue.put(OSError(f"ReadFile error {last_error}")); break
                elif bytes_read.value == 0: break # Assume EOF

                # Decode the raw bytes into a string using specified encoding
                raw_bytes = read_buffer.raw[:bytes_read.value]
                decoded_str = None
                try:
                    # Try primary encoding first
                    decoded_str = raw_bytes.decode(self.encoding, self.errors)
                except UnicodeDecodeError:
                    # Fall back to secondary encoding if primary fails
                    try: decoded_str = raw_bytes.decode(self.fallback_encoding, 'replace')
                    except Exception: self._read_queue.put(UnicodeDecodeError("conpty", raw_bytes, 0, len(raw_bytes),"Both failed"))
                except Exception as e: self._read_queue.put(e)

                # Put decoded string in queue for main thread to consume
                if decoded_str is not None: self._read_queue.put(decoded_str)

        except Exception as e: self._read_queue.put(e)  # Forward any exceptions to main thread
        finally: 
            # Signal EOF to main thread
            self._read_queue.put(None)
            # log("ConPTY: Reader thread finished.") # Optional

    def _monitor_loop(self):
        """
        Monitor thread function that watches for child process termination.
        
        This runs in a separate thread to allow asynchronous monitoring of the 
        child process state. When the process exits, it updates the spawn instance's
        status fields and signals the process_ended_event.
        
        Thread-safety is maintained using the _state_lock when updating shared state.
        """
        # log(f"ConPTY: Monitor thread started for PID {self.pid}") # Optional
        exit_code_val = -1
        h_process_val = INVALID_HANDLE_VALUE
        try:
            with self._state_lock: # Safely get handle value
                 if self._proc_info.hProcess.value != INVALID_HANDLE_VALUE:
                      h_process_val = self._proc_info.hProcess.value

            if h_process_val != INVALID_HANDLE_VALUE:
                 h_process = HANDLE(h_process_val)
                 # Wait for the process to exit
                 WaitForSingleObject(h_process, INFINITE)
                 # Get exit code after wait completes
                 exit_code_dword = DWORD()
                 if GetExitCodeProcess(h_process, ctypes.byref(exit_code_dword)):
                     exit_code_val = exit_code_dword.value
                 # else: log error # Optional
            # else: log("Monitor loop: Invalid process handle") # Optional

        except Exception as e: pass # log error # Optional
        finally:
             # Update process state under lock
             with self._state_lock:
                self.status = exit_code_val
                self.exitstatus = exit_code_val
                self.terminated = True
                self.flag_eof = True
             # Signal that the process has ended
             self._process_ended_event.set()
             # log(f"ConPTY: Monitor thread finished (exit code: {self.exitstatus}).") # Optional

    def _drain_queues(self):
        # log("ConPTY: Draining queues") # Optional
        with self._state_lock: # Protect buffer access
            while True:
                try:
                    chunk = self._read_queue.get(block=False)
                    if chunk is None: self.flag_eof = True; break
                    elif isinstance(chunk, Exception): self.flag_eof = True; break
                    else: self.buffer += chunk
                except queue.Empty: break
                except Exception: break

    def _log_read(self, data):
        """
        Log data read from the child process.
        Used by read_nonblocking to log data to the logfile or logfile_read.
        """
        if self.logfile is not None:
            try:
                self.logfile.write(data)
                self.logfile.flush()
            except (TypeError, ValueError):
                # Fallback for files that expect bytes (Python 2 compatibility)
                self.logfile.write(data.encode(self.encoding, self.errors))
                self.logfile.flush()
                
        if self.logfile_read is not None:
            try:
                self.logfile_read.write(data)
                self.logfile_read.flush()
            except (TypeError, ValueError):
                # Fallback for files that expect bytes
                self.logfile_read.write(data.encode(self.encoding, self.errors))
                self.logfile_read.flush()

    def isalive(self):
        """
        Test if the child process is still running.
        
        If the process was already marked as terminated, returns False.
        Otherwise, checks the process status and updates state if needed.
        
        Returns:
            bool: True if the child process is still running, False otherwise
        """
        with self._state_lock:
            if self.terminated:
                return False
                
            # If process handle is invalid, process can't be alive
            if self._proc_info.hProcess.value == INVALID_HANDLE_VALUE:
                self.terminated = True
                return False
                
            # Check if process is still active
            exit_code = DWORD()
            if GetExitCodeProcess(self._proc_info.hProcess, ctypes.byref(exit_code)):
                if exit_code.value == STILL_ACTIVE:
                    return True
                else:
                    # Process has exited, update state
                    self.exitstatus = exit_code.value
                    self.status = exit_code.value
                    self.terminated = True
                    self.flag_eof = True
                    return False
            else:
                # Error getting exit code, assume process is dead
                self.terminated = True
                self.flag_eof = True
                return False

    def close(self, force=True):
        """
        Close the child process and clean up resources.
        
        Args:
            force (bool): If True (default), forcibly terminate the process if it's still running
            
        Returns:
            bool: True if successfully terminated, False otherwise
        """
        if self.closed:
            return True
            
        if self.isalive():
            if force:
                # Try to terminate the process if it's still running
                try:
                    if self._proc_info.hProcess.value != INVALID_HANDLE_VALUE:
                        TerminateProcess(self._proc_info.hProcess, 1)
                except Exception:
                    pass
                    
                # Wait a bit for the process to terminate
                time.sleep(self.delayafterterminate)
                
                # Check if process has terminated
                if self.isalive():
                    return False
                    
        # Clean up resources
        self._cleanup_handles()
        self.closed = True
        return True

    def __del__(self):
        if not getattr(self, 'closed', True): # Check if closed exists and is false
            try: self.close(force=True)
            except Exception: pass

    # --- Core Pexpect Methods ---
    # Using implementations from Claude's refinement
    def read_nonblocking(self, size=1, timeout=-1):
        with self._state_lock: # Protect state checks
            if self.closed: raise ValueError("I/O operation on closed file.")
            if self.flag_eof and not self.buffer: raise EOF("End Of File")

        if timeout == -1: timeout = self.timeout
        deadline = None
        if timeout is not None: deadline = time.monotonic() + timeout

        while True: # Loop until data, EOF, or timeout
            with self._state_lock: # Protect buffer access
                if len(self.buffer) >= size:
                    read_data = self.buffer[:size]; self.buffer = self.buffer[size:]
                    self._log_read(read_data); return read_data
                if self.flag_eof: # If EOF and buffer has less than size
                    read_data = self.buffer; self.buffer = ""
                    self._log_read(read_data)
                    if read_data: return read_data
                    else: raise EOF("End Of File")

            # Need more data, try queue
            current_time = time.monotonic()
            remaining_timeout = None
            can_block = False
            if deadline is not None:
                remaining_timeout = deadline - current_time
                if remaining_timeout <= 0: raise TIMEOUT("Timeout exceeded.")
                can_block = True
            elif timeout == 0: remaining_timeout = 0; can_block = False # Non-blocking
            elif timeout is None: can_block = True; remaining_timeout = None # Block indefinitely

            try:
                chunk = self._read_queue.get(block=can_block, timeout=remaining_timeout)
                if chunk is None: # EOF marker
                    with self._state_lock: self.flag_eof = True; self.terminated = not self.isalive() # Update state
                    # Re-check buffer after marking EOF
                    with self._state_lock:
                        if self.buffer:
                            read_data = self.buffer[:size]; self.buffer = self.buffer[size:]
                            self._log_read(read_data); return read_data
                        raise EOF("End Of File (EOF marker received)")
                elif isinstance(chunk, Exception):
                    with self._state_lock: self.flag_eof = True
                    raise EOF(f"Reader thread error: {chunk}")
                else:
                    with self._state_lock: self.buffer += chunk # Add to buffer safely

            except queue.Empty:
                # Timeout or non-blocking check found nothing
                # Re-check process liveness under lock
                with self._state_lock: alive = self.isalive() # isalive updates flags if needed
                if not alive and self._read_queue.empty(): # Check queue again after isalive
                    with self._state_lock: # Re-acquire lock for buffer check
                        if self.buffer:
                             read_data = self.buffer[:size]; self.buffer = self.buffer[size:]
                             self._log_read(read_data); return read_data
                        raise EOF("End Of File (process terminated and queue empty)")
                # If timeout expired or was zero, raise TIMEOUT
                if timeout == 0 or (deadline is not None and time.monotonic() >= deadline):
                     with self._state_lock: # Protect buffer access
                          if self.buffer: # Return what we have if timeout expired
                               read_data = self.buffer[:size]; self.buffer = self.buffer[size:]
                               self._log_read(read_data); return read_data
                          raise TIMEOUT("Timeout exceeded.")
                # If timeout is None, loop again after a short sleep
                if timeout is None: time.sleep(0.01)