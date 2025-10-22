// ============================================
// LOGIN PAGE SCRIPT
// ============================================

document.addEventListener("DOMContentLoaded", () => {
    initializePasswordToggle()
    initializeFormValidation()
    initializeFormSubmission()
  })
  
  // ============================================
  // PASSWORD VISIBILITY TOGGLE
  // ============================================
  
  function initializePasswordToggle() {
    const passwordToggle = document.getElementById("passwordToggle")
    const passwordInput = document.getElementById("password")
  
    if (!passwordToggle || !passwordInput) return
  
    passwordToggle.addEventListener("click", function (e) {
      e.preventDefault()
  
      const isPassword = passwordInput.type === "password"
      passwordInput.type = isPassword ? "text" : "password"
  
      // Update aria-label
      this.setAttribute("aria-label", isPassword ? "Hide password" : "Show password")
  
      // Add visual feedback
      this.classList.toggle("active")
    })
  }
  
  // ============================================
  // FORM VALIDATION
  // ============================================
  
  function initializeFormValidation() {
    const form = document.getElementById("loginForm")
    if (!form) return
  
    const inputs = form.querySelectorAll(".form-input")
  
    inputs.forEach((input) => {
      // Real-time validation on blur
      input.addEventListener("blur", function () {
        validateField(this)
      })
  
      // Clear error on input
      input.addEventListener("input", function () {
        if (this.classList.contains("error")) {
          this.classList.remove("error")
          const errorMsg = this.parentElement.nextElementSibling
          if (errorMsg && errorMsg.classList.contains("form-error")) {
            errorMsg.remove()
          }
        }
      })
    })
  }
  
  function validateField(field) {
    const value = field.value.trim()
    const fieldName = field.name
    let isValid = true
    let errorMessage = ""
  
    if (!value) {
      isValid = false
      errorMessage = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} is required`
    } else if (fieldName === "username" && value.length < 3) {
      isValid = false
      errorMessage = "Username must be at least 3 characters"
    } else if (fieldName === "password" && value.length < 3) {
      isValid = false
      errorMessage = "A senha deve ter pelo menos 3 caracteres"
    }
  
    if (!isValid) {
      field.classList.add("error")
      const existingError = field.parentElement.nextElementSibling
      if (existingError && existingError.classList.contains("form-error")) {
        existingError.textContent = errorMessage
      } else {
        const errorEl = document.createElement("span")
        errorEl.className = "form-error"
        errorEl.textContent = errorMessage
        field.parentElement.parentElement.appendChild(errorEl)
      }
    } else {
      field.classList.remove("error")
      const errorMsg = field.parentElement.nextElementSibling
      if (errorMsg && errorMsg.classList.contains("form-error")) {
        errorMsg.remove()
      }
    }
  
    return isValid
  }
  
  // ============================================
  // FORM SUBMISSION
  // ============================================
  
  function initializeFormSubmission() {
    const form = document.getElementById("loginForm")
    if (!form) return
  
    form.addEventListener("submit", function (e) {
      const inputs = this.querySelectorAll(".form-input")
      let isFormValid = true
  
      inputs.forEach((input) => {
        if (!validateField(input)) {
          isFormValid = false
        }
      })
  
      if (!isFormValid) {
        e.preventDefault()
        console.log("[v0] Form validation failed")
      } else {
        // Add loading state to button
        const submitBtn = form.querySelector('button[type="submit"]')
        if (submitBtn) {
          submitBtn.disabled = true
          submitBtn.classList.add("loading")
          const originalText = submitBtn.querySelector(".btn-text").textContent
          submitBtn.querySelector(".btn-text").textContent = "Signing in..."
        }
      }
    })
  }
  
  // ============================================
  // UTILITY FUNCTIONS
  // ============================================
  
  // Add error class styling
  const style = document.createElement("style")
  style.textContent = `
      .form-input.error {
          border-color: #ef4444;
          background-color: rgba(239, 68, 68, 0.05);
      }
  
      .form-input.error:focus {
          box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
      }
  
      .password-toggle.active {
          color: #2563eb;
      }
  
      .btn.loading {
          opacity: 0.7;
      }
  `
  document.head.appendChild(style)
  
  console.log("[v0] Login script initialized")
  