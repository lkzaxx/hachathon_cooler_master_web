<template>
  <transition name="fade">
    <div v-if="isVisible" class="popup-overlay" @click.self="closePopup">
      <div class="popup-content">
        <button class="close-btn" @click="closePopup">&times;</button>
        <div class="popup-body saved-layout">
          <!-- Left Column: Prompt -->
          <div class="left-column">
            <div class="section-title">目前選擇的Prompt</div>
            <div class="prompt-display-block">
              <button class="copy-prompt-btn" @click="copyPrompt" title="複製提示">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 01-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 011.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 00-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 01-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 00-3.375-3.375h-1.5a1.125 1.125 0 01-1.125-1.125v-1.5a3.375 3.375 0 00-3.375-3.375H9.75" />
                </svg>
              </button>
              <p>{{ imageData?.prompt || 'No prompt available.' }}</p>
            </div>
          </div>
          

          <!-- Middle Column: Image -->
          <div class="middle-column">
            <div class="main-image-block">
              <img v-if="imageData?.url" :src="imageData.url" alt="Saved Item Image" class="popup-image-preview" />
              <span v-else>No Image Available</span>
            </div>
          </div>

          <!-- Right Column: Parameters -->
          <div class="right-column">
             <div v-for="(value, key) in imageData?.filters" :key="key" class="param-display-item">
                <span class="param-label">{{ getFilterLabel(key) }}:</span>
                <span class="param-value">{{ value }}</span>
             </div>
             <div v-if="!imageData?.filters || Object.keys(imageData.filters).length === 0" class="no-filters">
                No parameters available.
             </div>
          </div>
        </div>
        <div class="popup-footer">
          <button class="back-btn" @click="closePopup">返回</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'SavedItemInfoPopup',
  props: {
    isVisible: {
      type: Boolean,
      required: true
    },
    imageData: {
      type: Object,
      default: () => ({ url: null, prompt: null, filters: {} })
    }
  },
  emits: ['close'],
  methods: {
    closePopup() {
      this.$emit('close');
    },
    getFilterLabel(key) {
      // Re-use the label mapping logic
      const labels = {
          style: '風格主題',
          material: '框架材質',
          sidePanel: '側板結構',
          lighting: '光效樣式',
          interior: '內部展示',
          design: '整體設計'
      };
      return labels[key] || key.charAt(0).toUpperCase() + key.slice(1); // Capitalize key if no label
    },
    async copyPrompt() { // Added async for clipboard API
      const promptText = this.imageData?.prompt;
      if (!promptText) {
        console.warn('No prompt text to copy.');
        // Optionally show a user message
        return;
      }
      try {
        await navigator.clipboard.writeText(promptText);
        console.log('Prompt copied to clipboard!');
        // Optionally show a success message to the user (e.g., tooltip)
      } catch (err) {
        console.error('Failed to copy prompt: ', err);
        // Optionally show an error message to the user
      }
    }
  }
}
</script>

<style scoped>
/* Base Popup Styles (similar to ImageInfoPopup) */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100; /* Ensure it's above other elements */
}

.popup-content {
  background-color: #1f1f1f;
  color: #fff;
  padding: 2rem;
  border-radius: 16px;
  position: relative;
  width: 85vw;
  max-width: 1100px; /* Slightly smaller max-width */
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
}

.close-btn {
  position: absolute;
  top: 0.8rem;
  right: 0.8rem;
  background: none;
  border: none;
  color: #aaa;
  font-size: 1.6rem;
  cursor: pointer;
  line-height: 1;
  padding: 0.2rem;
}

.close-btn:hover {
  color: #fff;
}

/* Layout for this specific popup */
.popup-body.saved-layout {
  display: grid;
  grid-template-columns: 1fr 1.5fr 1fr; /* Adjust column proportions */
  gap: 1.5rem;
  padding: 1rem 0;
  flex-grow: 1;
  align-items: flex-start; /* Align items to the top */
}

.left-column,
.middle-column,
.right-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.middle-column {
  align-items: center;
}

.section-title {
  font-size: 1.1rem;
  color: #eee;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

/* Left Column: Prompt Display */
.prompt-display-block {
  background-color: #333;
  border-radius: 8px;
  padding: 1rem;
  color: #ddd;
  font-size: 0.95rem;
  line-height: 1.5;
  word-break: break-word;
  min-height: 150px; /* Ensure some height */
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #444;
  position: relative; /* Needed for copy button positioning */
  padding-right: 3rem; /* Add padding to avoid overlap with button */
}

/* Copy Button Style */
.copy-prompt-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ccc;
  border-radius: 4px;
  padding: 0.3rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s, color 0.2s;
}

.copy-prompt-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.copy-prompt-btn svg {
  width: 16px;
  height: 16px;
}

/* Middle Column: Image Display */
.main-image-block {
  width: 100%;
  max-width: 400px;
  aspect-ratio: 1 / 1; /* Make it square */
  background-color: #444;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.popup-image-preview {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
}

/* Right Column: Parameters Display */
.right-column {
    background-color: #2a2a2a;
    padding: 1rem;
    border-radius: 8px;
}

.param-display-item {
    background-color: #383838;
    padding: 0.6rem 1rem;
    border-radius: 6px;
    margin-bottom: 0.6rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.param-label {
    color: #bbb;
    font-size: 0.9rem;
    margin-right: 0.5rem;
}

.param-value {
    color: #fff;
    font-weight: bold;
    font-size: 0.95rem;
}

.no-filters {
    color: #888;
    font-style: italic;
    font-size: 0.9rem;
    text-align: center;
    padding: 1rem;
}

/* Footer */
.popup-footer {
  text-align: center; /* Center the button */
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #333;
}

.back-btn {
  background: #f5e6f7;
  color: #333;
  border: none;
  border-radius: 10px;
  padding: 0.7em 2.2em;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.back-btn:hover {
  background: #e0c6f0;
}

/* Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 