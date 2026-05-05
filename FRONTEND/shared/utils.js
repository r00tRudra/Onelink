/* ─────────────────────────────────────────
   SHARED UTILITIES
   ───────────────────────────────────────── */

// ── API Configuration ──
const API_URL = window.ONELINK_API_URL || 'http://localhost:8000';
const FRONTEND_URL = window.ONELINK_FRONTEND_URL || window.location.origin;

// ── Authentication ──
const Auth = {
  getToken() {
    return localStorage.getItem('access_token');
  },

  getUser() {
    try {
      return JSON.parse(localStorage.getItem('auth_user'));
    } catch {
      return null;
    }
  },

  isAuthenticated() {
    return !!this.getToken();
  },

  setToken(token) {
    localStorage.setItem('access_token', token);
  },

  setUser(user) {
    localStorage.setItem('auth_user', JSON.stringify(user));
  },

  clear() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('auth_user');
  },

  logout() {
    this.clear();
    window.location.href = '../auth/sign-in.html';
  }
};

// ── UI Utilities ──
const UI = {
  showToast(message, duration = 2800) {
    const toast = document.getElementById('toast');
    if (!toast) return;

    const toastMsg = document.getElementById('toastMsg');
    if (toastMsg) toastMsg.textContent = message;

    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), duration);
  },

  showLoading(element) {
    if (element) element.classList.add('loading');
  },

  hideLoading(element) {
    if (element) element.classList.remove('loading');
  },

  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('open');
  },

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('open');
  },

  toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.toggle('open');
  }
};

// ── DOM Utilities ──
const DOM = {
  qs(selector) {
    return document.querySelector(selector);
  },

  qsa(selector) {
    return document.querySelectorAll(selector);
  },

  byId(id) {
    return document.getElementById(id);
  },

  show(element) {
    if (element) element.style.display = '';
  },

  hide(element) {
    if (element) element.style.display = 'none';
  },

  toggle(element) {
    if (element) {
      element.style.display = element.style.display === 'none' ? '' : 'none';
    }
  },

  addClass(element, className) {
    if (element) element.classList.add(className);
  },

  removeClass(element, className) {
    if (element) element.classList.remove(className);
  },

  toggleClass(element, className) {
    if (element) element.classList.toggle(className);
  },

  hasClass(element, className) {
    return element ? element.classList.contains(className) : false;
  },

  setText(element, text) {
    if (element) element.textContent = text;
  },

  setHTML(element, html) {
    if (element) element.innerHTML = html;
  },

  setAttribute(element, attr, value) {
    if (element) element.setAttribute(attr, value);
  },

  getAttribute(element, attr) {
    return element ? element.getAttribute(attr) : null;
  },

  on(element, event, handler) {
    if (element) element.addEventListener(event, handler);
  },

  off(element, event, handler) {
    if (element) element.removeEventListener(event, handler);
  }
};

// ── URL Parameters ──
const URL = {
  getParam(key) {
    return new URLSearchParams(window.location.search).get(key);
  },

  getParams() {
    const params = {};
    new URLSearchParams(window.location.search).forEach((value, key) => {
      params[key] = value;
    });
    return params;
  },

  setParam(key, value) {
    const params = new URLSearchParams(window.location.search);
    params.set(key, value);
    window.history.replaceState({}, '', `?${params.toString()}`);
  }
};

// ── Storage ──
const Storage = {
  set(key, value) {
    try {
      if (typeof value === 'object') {
        localStorage.setItem(key, JSON.stringify(value));
      } else {
        localStorage.setItem(key, value);
      }
    } catch (e) {
      console.error('Storage error:', e);
    }
  },

  get(key) {
    try {
      const value = localStorage.getItem(key);
      if (!value) return null;
      try {
        return JSON.parse(value);
      } catch {
        return value;
      }
    } catch (e) {
      console.error('Storage error:', e);
      return null;
    }
  },

  remove(key) {
    try {
      localStorage.removeItem(key);
    } catch (e) {
      console.error('Storage error:', e);
    }
  },

  clear() {
    try {
      localStorage.clear();
    } catch (e) {
      console.error('Storage error:', e);
    }
  }
};

// ── Intersection Observer for Reveal Animations ──
const Observer = {
  initReveal(threshold = 0.12) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold }
    );

    document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
  }
};

// ── Debounce & Throttle ──
const Timing = {
  debounce(func, delay = 300) {
    let timeoutId;
    return function (...args) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
  },

  throttle(func, limit = 300) {
    let lastFunc;
    let lastRan;
    return function (...args) {
      if (!lastRan) {
        func.apply(this, args);
        lastRan = Date.now();
      } else {
        clearTimeout(lastFunc);
        lastFunc = setTimeout(() => {
          if (Date.now() - lastRan >= limit) {
            func.apply(this, args);
            lastRan = Date.now();
          }
        }, limit - (Date.now() - lastRan));
      }
    };
  }
};

// ── API Calls ──
const API = {
  async get(endpoint) {
    try {
      const fullURL = `${API_URL}${endpoint}`;
      const headers = {
        'Authorization': `Bearer ${Auth.getToken()}`,
        'Content-Type': 'application/json'
      };
      
      console.log('[API GET]', fullURL, 'Headers:', headers);
      
      const response = await fetch(fullURL, { headers });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('[API ERROR]', response.status, errorText);
        throw new Error(`API Error ${response.status}: ${errorText}`);
      }
      
      const data = await response.json();
      console.log('[API RESPONSE]', endpoint, data);
      return data;
    } catch (error) {
      console.error('[API GET ERROR]', endpoint, error);
      throw error;
    }
  },

  async post(endpoint, data) {
    try {
      const fullURL = `${API_URL}${endpoint}`;
      const headers = {
        'Authorization': `Bearer ${Auth.getToken()}`,
        'Content-Type': 'application/json'
      };
      
      console.log('[API POST]', fullURL, 'Data:', data);
      
      const response = await fetch(fullURL, {
        method: 'POST',
        headers,
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('[API ERROR]', response.status, errorText);
        throw new Error(`API Error ${response.status}: ${errorText}`);
      }
      
      const responseData = await response.json();
      console.log('[API RESPONSE]', endpoint, responseData);
      return responseData;
    } catch (error) {
      console.error('[API POST ERROR]', endpoint, error);
      throw error;
    }
  },

  async put(endpoint, data) {
    try {
      const fullURL = `${API_URL}${endpoint}`;
      const headers = {
        'Authorization': `Bearer ${Auth.getToken()}`,
        'Content-Type': 'application/json'
      };
      
      console.log('[API PUT]', fullURL, 'Data:', data);
      
      const response = await fetch(fullURL, {
        method: 'PUT',
        headers,
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('[API ERROR]', response.status, errorText);
        throw new Error(`API Error ${response.status}: ${errorText}`);
      }
      
      const responseData = await response.json();
      console.log('[API RESPONSE]', endpoint, responseData);
      return responseData;
    } catch (error) {
      console.error('[API PUT ERROR]', endpoint, error);
      throw error;
    }
  },

  async delete(endpoint) {
    try {
      const fullURL = `${API_URL}${endpoint}`;
      const headers = {
        'Authorization': `Bearer ${Auth.getToken()}`,
        'Content-Type': 'application/json'
      };
      
      console.log('[API DELETE]', fullURL);
      
      const response = await fetch(fullURL, {
        method: 'DELETE',
        headers
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('[API ERROR]', response.status, errorText);
        throw new Error(`API Error ${response.status}: ${errorText}`);
      }
      
      const responseData = await response.json();
      console.log('[API RESPONSE]', endpoint, responseData);
      return responseData;
    } catch (error) {
      console.error('[API DELETE ERROR]', endpoint, error);
      throw error;
    }
  }
};

// Export for module usage (if needed)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Auth, UI, DOM, URL, Storage, Observer, Timing, API };
}
