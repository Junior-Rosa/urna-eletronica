/**
 * Toast Notification System
 * Usage: window.showToast('Success!', 'success', 3000)
 */

window.showToast = (message, type = "info", duration = 3000) => {
    const container = document.getElementById("toast-container")
    const template = document.getElementById("toast-template")
  
    if (!container || !template) {
      console.error("[v0] Toast container or template not found")
      return
    }
  
    // Clone the template
    const toast = template.content.cloneNode(true)
    const toastElement = toast.querySelector(".toast")
  
    // Set type and message
    toastElement.classList.add(type)
    toast.querySelector(".toast-message").textContent = message
  
    // Add to container
    container.appendChild(toast)
    const toastNode = container.lastElementChild
  
    // Close button functionality
    const closeBtn = toastNode.querySelector(".toast-close")
    const removeToast = () => {
      toastNode.classList.add("removing")
      setTimeout(() => toastNode.remove(), 300)
    }
  
    closeBtn.addEventListener("click", removeToast)
  
    // Auto-remove after duration
    if (duration > 0) {
      setTimeout(removeToast, duration)
    }
  }
  
  // Convenience methods
  window.toastSuccess = (message, duration = 3000) => window.showToast(message, "success", duration)
  window.toastError = (message, duration = 3000) => window.showToast(message, "error", duration)
  window.toastWarning = (message, duration = 3000) => window.showToast(message, "warning", duration)
  window.toastInfo = (message, duration = 3000) => window.showToast(message, "info", duration)
  