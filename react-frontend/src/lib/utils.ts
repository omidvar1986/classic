import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Lightweight toast utility for nicer notifications without a dependency
export function showToast(message: string, type: 'success' | 'error' | 'info' = 'info') {
  try {
    const containerId = 'app-toast-container';
    let container = document.getElementById(containerId);
    if (!container) {
      container = document.createElement('div');
      container.id = containerId;
      container.style.position = 'fixed';
      container.style.top = '16px';
      container.style.right = '16px';
      container.style.display = 'flex';
      container.style.flexDirection = 'column';
      container.style.gap = '8px';
      container.style.zIndex = '9999';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.style.padding = '12px 16px';
    toast.style.borderRadius = '10px';
    toast.style.color = '#ffffff';
    toast.style.fontSize = '14px';
    toast.style.boxShadow = '0 8px 24px rgba(0,0,0,0.3)';
    toast.style.backdropFilter = 'blur(6px)';
    toast.style.border = '1px solid rgba(255,255,255,0.15)';
    toast.style.maxWidth = '360px';
    toast.style.lineHeight = '1.5';
    toast.style.transition = 'transform 0.2s ease, opacity 0.2s ease';
    toast.style.transform = 'translateY(-8px)';
    toast.style.opacity = '0';

    const bgByType = {
      success: 'linear-gradient(135deg, rgba(16,185,129,0.95), rgba(5,150,105,0.95))',
      error: 'linear-gradient(135deg, rgba(239,68,68,0.95), rgba(185,28,28,0.95))',
      info: 'linear-gradient(135deg, rgba(59,130,246,0.95), rgba(29,78,216,0.95))',
    } as const;
    toast.style.background = bgByType[type] || bgByType.info;

    toast.textContent = message;
    container.appendChild(toast);

    requestAnimationFrame(() => {
      toast.style.transform = 'translateY(0)';
      toast.style.opacity = '1';
    });

    const remove = () => {
      toast.style.transform = 'translateY(-8px)';
      toast.style.opacity = '0';
      setTimeout(() => {
        try { container?.removeChild(toast); } catch {}
      }, 180);
    };

    setTimeout(remove, 3000);
    toast.addEventListener('click', remove);
  } catch (err) {
    // Fallback if DOM not available
    console.log(message);
  }
}
