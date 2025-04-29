<template>
  <transition name="fade">
    <div v-if="isVisible" class="popup-overlay" @click.self="$emit('close')">
      <div class="popup-content">
        <button class="close-btn" @click="$emit('close')">&times;</button>
        <div class="case-view-buttons">
          <button
            v-for="(label, idx) in ['機殼全部', '機殼正面', '機殼側面']"
            :key="idx"
            :class="{ selected: selectedCaseView === idx }"
            @click="selectedCaseView = idx"
          >
            {{ label }}
          </button>
        </div>
        <div class="popup-body layout-frame7">
          <!-- 左側：Prompt/Negative prompt -->
          <div class="left-column">
            <div class="prompt-section">
              <div class="section-title">個人化提示修改</div>
              <div class="prompt-block">
                <textarea
                  v-model="editablePrompt"
                  placeholder="請輸入個人化提示..."
                />
              </div>
            </div>
            <div class="prompt-section">
              <div class="section-title">個人化否定提示 (不想出現的內容)</div>
              <div class="prompt-block negative-block">
                <textarea
                  v-model="editableNegativePrompt"
                  placeholder="請輸入不想出現的內容..."
                />
              </div>
            </div>
            <div class="prompt-section">
              <div class="section-title">目前選擇的Prompt</div>
              <div class="prompt-block current-prompt">
                <!-- 可加入當前Prompt -->
              </div>
              <button class="confirm-btn-small">確認</button>
            </div>
          </div>

          <!-- 中間：主圖＋縮圖＋Timeline -->
          <div class="middle-column">
            <div class="main-image-block">
              <img
                v-if="imageData?.url"
                :src="imageData.url"
                alt="Image Info"
                class="popup-image-preview"
              />
              <span v-else>No Image Available</span>
              <button
                v-if="imageData?.url"
                class="favorite-btn"
                :class="{ favorited: isFavorite }"
                @click="isFavorite = !isFavorite"
              >
                <svg
                  v-if="!isFavorite"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
                  />
                </svg>
                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.218l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z"
                  />
                </svg>
              </button>
            </div>
            <div class="small-image-row">
              <div
                v-for="(img, i) in smallImages"
                :key="i"
                class="small-image-block"
                style="position: relative"
              >
                <img
                  v-if="img"
                  :src="img"
                  style="
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    border-radius: 8px;
                  "
                />
                <button
                  v-if="img"
                  class="favorite-btn"
                  :class="{ favorited: isFavoriteSmall[i] }"
                  @click="isFavoriteSmall[i] = !isFavoriteSmall[i]"
                  style="right: 0.6rem; bottom: 0.6rem"
                >
                  <svg
                    v-if="!isFavoriteSmall[i]"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
                    />
                  </svg>
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.218l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z"
                    />
                  </svg>
                </button>
              </div>
            </div>
            <div class="timeline-section">
              <button class="generate-btn" @click="handleGenerate()" title="生成預覽圖 (3張)">
                開始生成(左側)
              </button>
              <button class="generate-btn home-style-btn" @click="handleGenerateHomeStyle()" title="生成至下方圖庫 (8張)">
                開始生成(右側)
              </button>
              <hr class="timeline-divider" />
              <div class="timeline-title">Timeline</div>
            </div>
          </div>

          <!-- 右側：參數選單 -->
          <div class="right-column">
            <div class="param-group">
              <label>風格主題</label>
              <select class="filter-select" v-model="selectedStyle">
                <option value="">隨機</option>
                <option v-for="opt in styles" :key="opt.id" :value="opt.id">{{ opt.name }}</option>
              </select>
            </div>
            <div class="param-group">
              <label>框架材質</label>
              <select class="filter-select" v-model="selectedMaterial">
                <option value="">隨機</option>
                <option v-for="opt in materials" :key="opt.id" :value="opt.id">{{ opt.name }}</option>
              </select>
            </div>
            <div class="param-group">
              <label>側板結構</label>
              <select class="filter-select" v-model="selectedSidePanel">
                <option value="">隨機</option>
                <option v-for="opt in sidePanels" :key="opt.id" :value="opt.id">{{ opt.name }}</option>
              </select>
            </div>
            <div class="param-group">
              <label>光效樣式</label>
              <select class="filter-select" v-model="selectedLighting">
                <option value="">隨機</option>
                <option v-for="opt in lighting" :key="opt.id" :value="opt.id">{{ opt.name }}</option>
              </select>
            </div>
            <div class="param-group">
              <label>內部展示</label>
              <select class="filter-select" v-model="selectedInterior">
                <option value="">隨機</option>
                <option v-for="opt in interiors" :key="opt.id" :value="opt.id">{{ opt.name }}</option>
              </select>
            </div>
            <div class="param-group">
              <label>整體設計</label>
              <select class="filter-select" v-model="selectedDesign">
                <option value="">隨機</option>
                <option v-for="opt in designs" :key="opt.id" :value="opt.id">{{ opt.name }}</option>
              </select>
            </div>
          </div>
        </div>
        <div class="generated-gallery-container">
          <div
            v-for="(img, i) in galleryImages"
            :key="i"
            class="gallery-item"
            style="position: relative"
          >
            <img
              v-if="img"
              :src="img"
              style="
                width: 100%;
                height: 100%;
                object-fit: cover;
                border-radius: 8px;
              "
            />
            <button
              v-if="img"
              class="favorite-btn"
              :class="{ favorited: isFavoriteGallery[i] }"
              @click="isFavoriteGallery[i] = !isFavoriteGallery[i]"
              style="right: 0.6rem; bottom: 0.6rem"
            >
              <svg
                v-if="!isFavoriteGallery[i]"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
                />
              </svg>
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.218l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z"
                />
              </svg>
            </button>
          </div>
        </div>
        <div class="popup-footer">
          <button class="confirm-btn" @click="$emit('close')">確認</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
// 工具函數：根據當前環境返回正確的API基礎URL
function getApiBaseUrl() {
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8080';
  } else {
    // 正式環境統一走 CloudFront
    return 'https://dq4ienvxghzmv.cloudfront.net';
  }
}

export default {
  name: "ImageInfoPopup",
  props: {
    isVisible: {
      type: Boolean,
      required: true,
    },
    imageData: {
      type: Object,
      default: () => ({ url: null, filters: null }),
    },
  },
  emits: ["close"],
  data() {
    return {
      styles: [
        { id: 1, name: "futuristic" },
        { id: 2, name: "minimalistic" },
        { id: 3, name: "industrial" },
        { id: 4, name: "cyberpunk" },
        { id: 5, name: "sci-fi" },
      ],
      materials: [
        { id: 1, name: "aluminum frame" },
        { id: 2, name: "steel-reinforced structure" },
        { id: 3, name: "titanium alloy" },
        { id: 4, name: "carbon fiber frame" },
        { id: 5, name: "lightweight magnesium frame" },
      ],
      sidePanels: [
        { id: 1, name: "tempered glass side panel" },
        { id: 2, name: "full mesh panel" },
        { id: 3, name: "solid aluminum side panel" },
        { id: 4, name: "perforated steel panel" },
        { id: 5, name: "acrylic transparent panel" },
      ],
      lighting: [
        { id: 1, name: "product photography lighting" },
        { id: 2, name: "natural sunlight" },
        { id: 3, name: "RGB studio lighting" },
        { id: 4, name: "ambient soft light" },
        { id: 5, name: "dark moody lighting" },
      ],
      interiors: [
        { id: 1, name: "high-end internal components visible" },
        { id: 2, name: "RGB lighting system" },
        { id: 3, name: "custom water cooling loop" },
        { id: 4, name: "clean cable management" },
        { id: 5, name: "minimalist build" },
      ],
      designs: [
        { id: 1, name: "stylish and sleek industrial design" },
        { id: 2, name: "minimalist front panel with hidden ports" },
        { id: 3, name: "aggressive gaming aesthetic" },
        { id: 4, name: "symmetrical futuristic design" },
        { id: 5, name: "vertical front vent design" },
      ],
      editablePrompt: "",
      editableNegativePrompt: "",
      selectedStyle: "",
      selectedMaterial: "",
      selectedSidePanel: "",
      selectedLighting: "",
      selectedInterior: "",
      selectedDesign: "",
      selectedCaseView: 0,
      isFavorite: false,
      smallImages: [null, null, null], // 之後可由 props 傳入
      isFavoriteSmall: [false, false, false],
      galleryImages: [null, null, null, null, null, null, null, null], // 之後可由 props 傳入
      isFavoriteGallery: [
        false,
        false,
        false,
        false,
        false,
        false,
        false,
        false,
      ],
    };
  },
  mounted() {
    this.editablePrompt = this.imageData?.prompt || "";
    this.editableNegativePrompt = this.imageData?.negativePrompt || "";
  },
  methods: {
    getImageFilename(url) {
      if (!url) return "N/A";
      try {
        const path = new URL(url, window.location.origin).pathname;
        return path.substring(path.lastIndexOf("/") + 1);
      } catch (e) {
        console.error("Error parsing URL for filename:", e);
        return String(url).includes("/") ? url : "Invalid URL";
      }
    },
    getFilterLabel(key) {
      const labels = {
        style: "風格主題",
        material: "框架材質",
        sidePanel: "側板結構",
        lighting: "光效樣式",
        interior: "內部展示",
        design: "整體設計",
      };
      return labels[key] || key;
    },
    applyPrompt() {
      // 可選：將編輯的 prompt 應用到主流程
      this.$emit("update:prompt", this.editablePrompt);
      this.$emit("update:negative-prompt", this.editableNegativePrompt);
    },
    async handleGenerate() {
      if (this.loading) return;
      this.loading = true;
      const getNameById = (id, options) => {
        if (!id) return null;
        const option = options.find(opt => opt.id === id);
        return option ? option.name : null;
      };
      try {
        // 收集選項的值
        const userSelections = {
          style: getNameById(this.selectedStyle, this.styles),
          material: getNameById(this.selectedMaterial, this.materials),
          sidePanel: getNameById(this.selectedSidePanel, this.sidePanels),
          lighting: getNameById(this.selectedLighting, this.lighting),
          interior: getNameById(this.selectedInterior, this.interiors),
          design: getNameById(this.selectedDesign, this.designs),
        };
        
        const payload = {
          userSelections: userSelections,
          case_view_mode: this.selectedCaseView,
          mask_mode: 0
        };
        
        // 根據環境自動選擇 API 地址
        let baseUrl = getApiBaseUrl();
        console.log(`目前環境: ${window.location.hostname}, 使用 API 基礎網址: ${baseUrl}`);
        console.log("Payload for Preview generation:", payload);
        // Use dynamic import for axios if not globally available
        const axiosInstance = this.$axios || (await import("axios")).default;
        const response = await axiosInstance.post(
          `${baseUrl}/api/generate-images/`, // 使用完整 API URL
          payload
        );
        if (response.data && Array.isArray(response.data.fileUrls)) {
          this.smallImages = response.data.fileUrls.slice(0, 3);
        } else {
          console.warn("API did not return expected fileUrls array:", response.data);
          alert("生成成功，但未獲得預期的圖片數據。");
        }
      } catch (error) {
        console.error("生成圖片時發生錯誤:", error);
        alert(
          "生成圖片時發生錯誤: " + (error.response?.data?.error || error.message)
        );
      } finally {
        this.loading = false;
      }
    },
    async handleGenerateHomeStyle() {
      if (this.loading) return;
      this.loading = true;
      const getNameById = (id, options) => {
        if (!id) return null;
        const option = options.find(opt => opt.id === id);
        return option ? option.name : null;
      };
      console.log("Triggering Home-style generation...");
      try {
        const userSelections = {
          style: getNameById(this.selectedStyle, this.styles),
          material: getNameById(this.selectedMaterial, this.materials),
          sidePanel: getNameById(this.selectedSidePanel, this.sidePanels),
          lighting: getNameById(this.selectedLighting, this.lighting),
          interior: getNameById(this.selectedInterior, this.interiors),
          design: getNameById(this.selectedDesign, this.designs),
        };
        
        const payload = {
          case_view_mode: this.selectedCaseView,
          userSelections: userSelections,
          mask_mode: 0
        };

        console.log("Payload for Home-style generation:", payload);
        
        // 根據環境自動選擇 API 地址
        let baseUrl = getApiBaseUrl();
        console.log(`目前環境: ${window.location.hostname}, 使用 API 基礎網址: ${baseUrl}`);

        const axiosInstance = this.$axios || (await import("axios")).default;
        const response = await axiosInstance.post(
          `${baseUrl}/api/generate-images/`,
          payload
        );

        if (response.data && Array.isArray(response.data.fileUrls)) {
          console.log("Received URLs for gallery:", response.data.fileUrls);
          
          // 處理圖片 URL - 將相對路徑轉換為絕對路徑
          const processedUrls = response.data.fileUrls.map(url => {
            // 如果是相對路徑，加上 baseUrl
            if (url && url.startsWith('/')) {
              return baseUrl + url;
            }
            // 如果已經是完整 URL 則直接返回
            return url;
          });
          
          console.log("Processed image URLs:", processedUrls);
          
          // Create objects for the gallery
          const newGalleryObjects = processedUrls.map(url => ({
            url: url, // Assuming backend returns full URLs or handles base path
            filters: { /* Store current filters if needed */ }
          }));
          // Replace the gallery content
          this.galleryImages = newGalleryObjects.slice(0, 8);
          this.isFavoriteGallery = Array(this.galleryImages.length).fill(false);
          
          // Update smallImages with returned URLs
          this.smallImages = processedUrls.slice(0, 3);
          if (this.smallImages.length > 0) {
            this.isFavoriteSmall = Array(this.smallImages.length).fill(false);
          }
          
          console.log("Updated galleryImages:", this.galleryImages);
        } else {
          console.warn("API did not return expected fileUrls array for home-style generation:", response.data);
          alert("主頁模式生成成功，但未獲得預期的圖片數據。");
        }

      } catch (error) {
        console.error("主頁模式生成圖片時發生錯誤:", error);
        alert(
          "主頁模式生成圖片時發生錯誤: " + (error.response?.data?.error || error.message)
        );
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.popup-content {
  background-color: #1f1f1f;
  color: #fff;
  padding: 2.5rem;
  border-radius: 12px;
  position: relative;
  width: 95vw;
  max-width: 1400px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: #ccc;
  font-size: 1.8rem;
  cursor: pointer;
  line-height: 1;
}

.close-btn:hover {
  color: #fff;
}

.popup-body.layout-frame7 {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 1.5rem;
  background-color: #1a1a1a;
  padding: 1.5rem;
  border-radius: 8px;
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.middle-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.right-column {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.section-title {
  font-size: 0.9rem;
  color: #fff;
  margin-bottom: 0.5rem;
}

.prompt-section {
  background-color: #3a3a3a;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
}

.prompt-block {
  background-color: #444;
  border-radius: 6px;
  padding: 0.8rem;
  min-height: 80px;
  color: #eee;
  font-size: 0.9rem;
  word-break: break-word;
}

.negative-block {
  background-color: #444;
  min-height: 40px;
}

.current-prompt {
  min-height: 80px;
}

.confirm-btn-small {
  margin-top: 0.5rem;
  align-self: flex-end;
  background-color: #4a0d7a;
  color: white;
  border: none;
  padding: 0.4rem 1rem;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
}

.main-image-block {
  width: 100%;
  height: 350px;
  background-color: #444;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
}

.popup-image-preview {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.small-image-row {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  width: 100%;
  margin-top: 1rem;
}

.small-image-block {
  flex: 1;
  aspect-ratio: 1 / 1;
  height: 200px;
  max-width: 2200px;
  background-color: #4a4a4a;
  border-radius: 8px;
}

.timeline-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.timeline-title {
  text-align: center;
  margin-bottom: 0.2rem;
  color: #ccc;
  font-size: 1rem;
}

.param-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.8rem;
}

.param-group label {
  color: #fff;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.filter-select {
  background-color: #eee;
  color: #333;
  border: none;
  padding: 0.6rem 0.8rem;
  border-radius: 4px;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke-width='2' stroke='%23333' class='w-6 h-6'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='m19.5 8.25-7.5 7.5-7.5-7.5' /%3E%3C/svg%3E%0A");
  background-repeat: no-repeat;
  background-position: right 0.5rem center;
  background-size: 1em;
  cursor: pointer;
}

.popup-footer {
  text-align: right;
  margin-top: 1rem;
}

.confirm-btn {
  background-color: #4a0d7a;
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.confirm-btn:hover {
  background-color: #6a1d9a;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.no-filters {
  color: #888;
  font-style: italic;
  font-size: 0.9rem;
  text-align: center;
  width: 100%;
}

.generate-btn {
  display: block;
  margin: 0 auto 1.2rem auto;
  background-color: #6a50a7;
  color: white;
  border: none;
  padding: 0.8rem 2.5rem;
  border-radius: 999px;
  font-size: 1.2rem;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.generate-btn:hover {
  background-color: #7b5fd6;
}

.home-style-btn {
  background-color: #5a4097;
}

.home-style-btn:hover {
  background-color: #6b50a7;
}

.generated-gallery-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  overflow-y: auto;
  padding: 2rem;
  border-radius: 16px;
  background-color: #303030;
  margin-top: 0.2rem;
  margin-bottom: 2rem;
  width: fit-content;
  min-width: 0;
  margin-left: auto;
  margin-right: auto;
}

.gallery-item {
  background-color: #444;
  border-radius: 8px;
  aspect-ratio: 1 / 1;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timeline-divider {
  border: none;
  border-top: 1px solid #444;
  margin: 1.2rem 0 0.5rem 0;
}

.prompt-block textarea,
.negative-block textarea {
  width: 100%;
  min-height: 60px;
  background: #444;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.8rem;
  font-size: 0.95rem;
  resize: vertical;
  outline: none;
}

.prompt-block textarea:focus,
.negative-block textarea:focus {
  background: #555;
}

.favorite-btn {
  position: absolute;
  right: 1.2rem;
  bottom: 1.2rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 2;
}

.favorite-btn svg {
  width: 32px;
  height: 32px;
  transition: fill 0.2s, stroke 0.2s;
}

.favorite-btn.favorited svg {
  fill: #e24a7a;
  stroke: #e24a7a;
}

.case-view-buttons {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 1.2rem;
}
.case-view-buttons button {
    background: #ccc;
    color: #333;
    border: none;
    border-radius: 12px;
    padding: 0.7em 1.7em;
    font-size: 1.1em;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
}
.case-view-buttons button:not(.selected) {
    background: #eee;
    color: #aaa;
}
.case-view-buttons button:hover {
    background: #bbb;
}
</style>
