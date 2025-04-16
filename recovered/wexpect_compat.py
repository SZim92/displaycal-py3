transition: all 0.3s ease;

      &:hover {
        background-color: rgba(86, 122, 149, 0.1);
        transform: translateX(3px);
      }
    }
  }
}

// Accessibility improvements
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #2a3542;
  color: white;
  padding: 8px;
  z-index: 100;

  &:focus {
    top: 0;
  }
}

// Improve focus visibility for keyboard users
a:focus,
button:focus,
input:focus,
select:focus,
textarea:focus,
.btn:focus {
  outline: 2px solid #567a95 !important;
  outline-offset: 2px;
}

// Footer customizations
.page__footer-accessibility {
  margin-top: 1em;
  padding-top: 1em;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;

  a {
    color: #f8f8f5;
    transition: color 0.3s ease;

    &:hover {
      text-decoration: underline;
      color: #fff;
    }
  }
}

// Ecosystem footer section
.page__footer-ecosystem {
  margin-bottom: 2em;
  padding-bottom: 1em;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  h4 {
    color: white;
    font-weight: 500;
    margin-bottom: 0.5em;
  }

  p {
    font-size: 0.9em;
    margin-bottom: 0.5em;
    opacity: 0.9;
  }

  ul {
    list-style-type: none;
    padding-left: 0;
    margin-left: 0;

    li {
      margin-bottom: 0.5em;
      font-size: 0.9em;

      a {
        font-weight: 500;
        transition: color 0.3s ease;

        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
}

// Typography enhancements
h1 {
  font-size: 2.75rem;
  font-weight: 600;
  letter-spacing: -0.25px;
}

h2 {
  font-size: 2rem;
  letter-spacing: -0.25px;
}

.intro {
  h1 {
    font-size: 2.75rem;
    font-weight: 600;
    letter-spacing: -0.25px;
    margin-bottom: 1.5rem;
  }

  p {
    font-size: 1.25rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }

  .value-proposition {
    font-size: 1.15rem;
    line-height: 1.5;
    color: #567a95;
    border-left: 3px solid #8a785d;
    padding-left: 1rem;

    .specialty {
      display: block;
      margin-top: 0.5rem;
      font-style: italic;
      font-size: 1rem;
    }
  }
}

// Section spacing improvements
section {
  padding: 3rem 0;
}

// Button enhancement
.btn {
  border: 2px solid #6c7a89;
  transition: all 0.3s ease;

  &:hover {
    background-color: #6c