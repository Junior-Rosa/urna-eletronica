/**
 * Global JavaScript for Django Template
 * Handles navigation, interactions, and utilities
 */

// ============================================
// MOBILE MENU TOGGLE
// ============================================

document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.querySelector(".menu-toggle")
    const nav = document.querySelector("nav")
  
    if (menuToggle) {
      menuToggle.addEventListener("click", () => {
        nav.classList.toggle("active")
  
        // Update button text/icon
        const isActive = nav.classList.contains("active")
        menuToggle.setAttribute("aria-expanded", isActive)
      })
  
      // Close menu when clicking on a link
      const navLinks = nav.querySelectorAll("a")
      navLinks.forEach((link) => {
        link.addEventListener("click", () => {
          nav.classList.remove("active")
          menuToggle.setAttribute("aria-expanded", "false")
        })
      })
  
      // Close menu when clicking outside
      document.addEventListener("click", (event) => {
        const isClickInsideNav = nav.contains(event.target)
        const isClickOnToggle = menuToggle.contains(event.target)
  
        if (!isClickInsideNav && !isClickOnToggle && nav.classList.contains("active")) {
          nav.classList.remove("active")
          menuToggle.setAttribute("aria-expanded", "false")
        }
      })
    }
  })
  
  // ============================================
  // SMOOTH SCROLL BEHAVIOR
  // ============================================
  
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const href = this.getAttribute("href")
      if (href !== "#") {
        e.preventDefault()
        const target = document.querySelector(href)
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start",
          })
        }
      }
    })
  })
  
  // ============================================
  // FORM VALIDATION
  // ============================================
  
  function validateForm(form) {
    let isValid = true
    const inputs = form.querySelectorAll("input, textarea, select")
  
    inputs.forEach((input) => {
      if (input.hasAttribute("required") && !input.value.trim()) {
        input.classList.add("error")
        isValid = false
      } else {
        input.classList.remove("error")
      }
  
      // Email validation
      if (input.type === "email" && input.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(input.value)) {
          input.classList.add("error")
          isValid = false
        }
      }
    })
  
    return isValid
  }
  
  // ============================================
  // ACTIVE NAVIGATION LINK
  // ============================================
  
  function setActiveNavLink() {
    const currentPath = window.location.pathname
    const navLinks = document.querySelectorAll("nav a")
  
    navLinks.forEach((link) => {
      const href = link.getAttribute("href")
      if (href === currentPath || (href !== "#" && currentPath.includes(href))) {
        link.classList.add("active")
      } else {
        link.classList.remove("active")
      }
    })
  }
  
  document.addEventListener("DOMContentLoaded", setActiveNavLink)
  
  // ============================================
  // LOADING STATE HANDLER
  // ============================================
  
  function setLoadingState(button, isLoading = true) {
    if (isLoading) {
      button.disabled = true
      button.dataset.originalText = button.textContent
      button.textContent = "Loading..."
      button.classList.add("loading")
    } else {
      button.disabled = false
      button.textContent = button.dataset.originalText || "Submit"
      button.classList.remove("loading")
    }
  }
  
  // ============================================
  // NOTIFICATION SYSTEM
  // ============================================
  
  function showNotification(message, type = "info", duration = 3000) {
    const notification = document.createElement("div")
    notification.className = `notification notification-${type}`
    notification.textContent = message
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 16px 24px;
      background-color: var(--color-${type});
      color: white;
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-lg);
      z-index: 1000;
      animation: slideIn 0.3s ease-in-out;
    `
  
    document.body.appendChild(notification)
  
    setTimeout(() => {
      notification.style.animation = "slideOut 0.3s ease-in-out"
      setTimeout(() => notification.remove(), 300)
    }, duration)
  }
  
  // ============================================
  // ANIMATIONS
  // ============================================
  
  const style = document.createElement("style")
  style.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
  
    @keyframes slideOut {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  
    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  
    .notification {
      animation: slideIn 0.3s ease-in-out;
    }
  
    button.loading {
      opacity: 0.7;
      cursor: not-allowed;
    }
  
    input.error,
    textarea.error,
    select.error {
      border-color: var(--color-error) !important;
      background-color: rgba(239, 68, 68, 0.05);
    }
  
    nav.active {
      animation: fadeIn 0.2s ease-in-out;
    }
  `
  document.head.appendChild(style)
  
  // ============================================
  // UTILITY FUNCTIONS
  // ============================================
  
  // Debounce function for performance
  function debounce(func, wait) {
    let timeout
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout)
        func(...args)
      }
      clearTimeout(timeout)
      timeout = setTimeout(later, wait)
    }
  }
  
  // Throttle function
  function throttle(func, limit) {
    let inThrottle
    return function (...args) {
      if (!inThrottle) {
        func.apply(this, args)
        inThrottle = true
        setTimeout(() => (inThrottle = false), limit)
      }
    }
  }
  
  // Export functions for use in other scripts
  window.djangoUtils = {
    validateForm,
    setLoadingState,
    showNotification,
    debounce,
    throttle,
  }
  