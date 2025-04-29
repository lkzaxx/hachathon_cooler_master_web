<template>
  <div class="home-container">
    <!-- Left Sidebar -->
    <aside class="sidebar">
      <nav class="menu">
        <ul>
          <li
            v-for="(item, index) in menuItems"
            :key="index"
            :class="{ active: activeMenuItem === index }"
            @click="handleMenuClick(index)"
          >
            {{ item }}
          </li>
        </ul>
      </nav>
    </aside>

    <!-- Main Content Area -->
    <main class="content-area">
      <!-- Top Row: Reference Images & Upload -->
      <div class="content-row top-row">
        <!-- 新增：目前選擇的參數方塊 -->
        <div class="content-box param-box">
          <div class="param-title">
            <h4>目前選擇的參數</h4>
          </div>
          <div class="param-content">
            <ul>
              <li>風格主題：{{ getSelectedName(style, styles) }}</li>
              <li>
                框架材質：{{ getSelectedName(chassis_frame, materials) }}
              </li>
              <li>
                側板結構：{{ getSelectedName(side_type, sidePanels) }}
              </li>
              <li>
                光效樣式：{{ getSelectedName(lighting_conditions, lighting) }}
              </li>
              <li>
                內部展示：{{ getSelectedName(interior_view, interiors) }}
              </li>
              <li>整體設計：{{ getSelectedName(front_layout, designs) }}</li>
            </ul>
          </div>
        </div>
        <div class="content-box image-box reference-box">
          <img
            v-if="
              referenceImageData &&
              referenceImageData.url &&
              referenceImageData.url !== PLACEHOLDER_REFERENCE_URL
            "
            :src="referenceImageData.url"
            alt="Reference Case Image"
          />
          <button
            v-if="
              referenceImageData &&
              referenceImageData.url &&
              referenceImageData.url !== PLACEHOLDER_REFERENCE_URL
            "
            class="favorite-btn"
            :class="{ favorited: isFavoriteReference }"
            @click.stop="isFavoriteReference = !isFavoriteReference"
            style="position: absolute; right: 1.2rem; bottom: 1.2rem"
          >
            <!-- Replaced Outline Heart -->
            <svg
              v-if="!isFavoriteReference"
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
            <!-- Replaced Solid Heart -->
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
          <span v-else-if="!referenceImageData || !referenceImageData.url"
            >Loading reference...</span>
          <!-- Action Button (Info only) -->
          <div class="image-actions">
            <button
              @click.stop="showInfo('reference', referenceImageData)"
              class="action-btn info-btn"
            >
              i
            </button>
          </div>
        </div>
        <div class="content-box upload-box" @click="triggerFileUpload">
          <input
            type="file"
            ref="fileInput"
            @change="handleFileChange"
            accept="image/*"
            style="display: none"
          />
          <!-- Show preview if available -->
          <template v-if="uploadedImagePreviewUrl">
            <img
              :src="uploadedImagePreviewUrl"
              alt="Uploaded Preview"
              class="uploaded-preview-img"
            />
            <!-- Action Buttons for Uploaded Image -->
            <div class="image-actions">
              <button
                @click.stop="triggerFileUpload"
                title="重新上傳"
                class="action-btn upload-replace-btn"
              >
                <!-- Re-use upload icon, smaller -->
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="2"
                  stroke="currentColor"
                  class="replace-upload-icon"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5"
                  />
                </svg>
              </button>
              <button
                @click.stop="clearUploadedImage"
                title="清除"
                class="action-btn delete-btn"
              >
                X
              </button>
            </div>
          </template>
          <!-- Otherwise, show default upload prompt -->
          <template v-else>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="upload-icon"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5"
              />
            </svg>
            <span>上傳參考圖片</span>
          </template>
        </div>
      </div>

      <!-- Second Row: Image Gallery (Clickable with Info Action) -->
      <div class="content-row gallery-row">
        <div
          v-for="(imgData, index) in galleryImages.slice(0, 4)"
          :key="'gallery-' + index"
          class="content-box image-box gallery-item"
          @click="swapReferenceWithGallery(index)"
          style="position: relative"
        >
          <img
            v-if="
              imgData && imgData.url && imgData.url !== PLACEHOLDER_DELETED_URL
            "
            :src="imgData.url"
            :alt="'Gallery Image ' + (index + 1)"
          />
          <button
            v-if="
              imgData && imgData.url && imgData.url !== PLACEHOLDER_DELETED_URL
            "
            class="favorite-btn"
            :class="{ favorited: isFavoriteGallery[index] }"
            @click.stop="isFavoriteGallery[index] = !isFavoriteGallery[index]"
            style="position: absolute; right: 1.2rem; bottom: 1.2rem"
          >
            <!-- Replaced Outline Heart -->
            <svg
              v-if="!isFavoriteGallery[index]"
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
            <!-- Replaced Solid Heart -->
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
          <!-- Handle loading/placeholder state based on url -->
          <span v-else>Loading...</span>
          <!-- Action Buttons (Info only for this row) -->
          <div class="image-actions">
            <!-- Pass index to showInfo -->
            <button
              @click.stop="showInfo('gallery', index)"
              class="action-btn info-btn"
            >
              i
            </button>
          </div>
        </div>
        <!-- Fill remaining slots if galleryImages has less than 4 items initially (shouldn't happen with current loadLocalImages) -->
        <template v-if="galleryImages.length < 4">
          <div
            v-for="i in 4 - galleryImages.length"
            :key="'gallery-placeholder-' + i"
            class="content-box image-box gallery-item placeholder-item"
          >
            <span>Empty Slot</span>
          </div>
        </template>
      </div>

      <!-- Third Row: Filters -->
      <div class="content-row filters-row">
        <div class="filter-group">
          <label>風格主題</label>
          <select v-model="style">
            <option value="">隨機</option>
            <option v-for="styleItem in styles" :key="styleItem.id" :value="styleItem.id">
              {{ styleItem.name }}
            </option>
          </select>
        </div>
        <div class="filter-group">
          <label>框架材質</label>
          <select v-model="chassis_frame">
            <option value="">隨機</option>
            <option
              v-for="material in materials"
              :key="material.id"
              :value="material.id"
            >
              {{ material.name }}
            </option>
          </select>
        </div>
        <div class="filter-group">
          <label>側板結構</label>
          <select v-model="side_type">
            <option value="">隨機</option>
            <option
              v-for="panel in sidePanels"
              :key="panel.id"
              :value="panel.id"
            >
              {{ panel.name }}
            </option>
          </select>
        </div>
      </div>
      <div class="content-row filters-row">
        <div class="filter-group">
          <label>光效樣式</label>
          <select v-model="lighting_conditions">
            <option value="">隨機</option>
            <option v-for="light in lighting" :key="light.id" :value="light.id">
              {{ light.name }}
            </option>
          </select>
        </div>
        <div class="filter-group">
          <label>內部展示</label>
          <select v-model="interior_view">
            <option value="">隨機</option>
            <option
              v-for="interior in interiors"
              :key="interior.id"
              :value="interior.id"
            >
              {{ interior.name }}
            </option>
          </select>
        </div>
        <div class="filter-group">
          <label>整體設計</label>
          <select v-model="front_layout">
            <option value="">隨機</option>
            <option
              v-for="design in designs"
              :key="design.id"
              :value="design.id"
            >
              {{ design.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Fourth Row: Generate Button -->
      <div class="content-row button-row">
        <button class="generate-btn" @click="generateImage">開始生成</button>
      </div>
    </main>

    <!-- Info Popup Component -->
    <image-info-popup
      :is-visible="showPopup"
      :image-data="selectedImageDataForPopup"
      @close="closeInfoPopup"
      :styles="styles"
      :materials="materials"
      :sidePanels="sidePanels"
      :lighting="lighting"
      :interiors="interiors"
      :designs="designs"
    >
    </image-info-popup>
  </div>
</template>

<script>
import axios from "axios";
// Removed Amplify import if only used for fetchImages previously
// import { API } from 'aws-amplify';

// Import the generated image list
import computerCaseImages from "@/computerCaseImages.json"; // Assuming the file is in src/
import ImageInfoPopup from "@/components/ImageInfoPopup.vue"; // Import the new component

// Helper function to shuffle an array
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

// 工具函數：根據當前環境返回正確的API基礎URL
function getApiBaseUrl() {
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8080';
  } else {
    // 正式環境統一走 CloudFront
    return 'https://dq4ienvxghzmv.cloudfront.net';
  }
}

const PLACEHOLDER_DELETED_URL =
  "https://via.placeholder.com/200/555555?text=Deleted";
const PLACEHOLDER_REFERENCE_URL =
  "https://via.placeholder.com/200/cccccc?text=Reference";

export default {
  name: "HomeView",
  components: {
    // Register the component
    ImageInfoPopup,
  },
  data() {
    return {
      // 添加缺少的常量
      PLACEHOLDER_DELETED_URL,
      PLACEHOLDER_REFERENCE_URL,
      // --- Local Computer Case Images ---
      // !!! IMPORTANT: Replace these filenames with your actual image filenames in public/Computer_Case/ !!!
      // caseImageFiles: [
      //   'case1.jpg', 'case2.jpg', 'case3.jpg', 'case4.jpg',
      //   'case5.jpg', 'case6.jpg', 'case7.jpg', 'case8.jpg',
      //   // Add more filenames if you have them
      // ],
      // Use the imported list instead
      caseImageFiles: computerCaseImages,
      galleryImages: [], // Holds objects { url: string, filters: object | null }
      generatedImages: [], // Holds objects { url: string, filters: object | null }
      // --- End Local Images ---

      // Removed 'images' array which was populated by fetchImages
      // images: [],
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
      style: "",
      chassis_frame: "",
      side_type: "",
      lighting_conditions: "",
      interior_view: "",
      front_layout: "",
      selectedImageCount: 1,
      menuItems: [
        "專案一 Cosmos",
        "專案二 MasterBox",
        "專案三 Cube",
        "專案四 NR200NX",
        "專案五 CubeBox",
        "專案六 New Comos",
        "儲存的專案",
      ],
      activeMenuItem: 0,
      isLoading: false, // Optional: for loading state during API calls
      // Popup state
      showPopup: false,
      selectedImageDataForPopup: null,
      // Add state for uploaded image preview
      uploadedImagePreviewUrl: null,
      referenceImageData: null, // Holds { url: string, filters: object | null }
      isFavoriteReference: false,
      isFavoriteGallery: [],
    };
  },
  created() {
    // Don't call fetchImages anymore for the gallery
    // this.fetchImages()
    this.loadLocalImages();
    // this.fetchCategories(); // Keep fetching categories // Commented out as options are now static
  },
  methods: {
    // Removed fetchImages method
    /*
    async fetchImages() {
      try {
        const response = await axios.get('http://localhost:8080/api/images/')
        this.images = response.data.map(img => ({
          ...img,
          imageUrl: 'http://localhost:8080' + img.image
        }))
        console.log("Fetched images:", this.images);
      } catch (error) {
        console.error('Error fetching images:', error)
        // Fallback removed as we now use local images
      }
    },
    */
    // --- Helper function to get random image URLs ---
    getRandomCaseImages(count) {
      if (!this.caseImageFiles || this.caseImageFiles.length === 0) {
        console.warn(
          "Cannot get random images: caseImageFiles is empty or not loaded."
        );
        // Return placeholders if no images available
        const placeholders = Array(count).fill(
          "https://via.placeholder.com/200/cccccc?text=No+Images"
        );
        return placeholders;
      }

      const shuffled = shuffleArray([...this.caseImageFiles]);
      const resultUrls = [];
      for (let i = 0; i < count; i++) {
        // Allow duplicates if count > available images
        const filename = shuffled[i % shuffled.length];
        resultUrls.push(`/img/Computer_Case/${filename}`);
      }
      return resultUrls;
    },
    // --- Update loadLocalImages to create objects with default filters ---
    loadLocalImages() {
      // Define default filters (all '隨機')
      const defaultFilters = {
        style: "隨機",
        material: "隨機",
        sidePanel: "隨機",
        lighting: "隨機",
        interior: "隨機",
        design: "隨機",
      };

      // 註解：隨機載入參考圖像
      /*
      // Get initial reference URL
      const randomRefUrls = this.getRandomCaseImages(1);
      if (
        randomRefUrls.length > 0 &&
        randomRefUrls[0] &&
        !randomRefUrls[0].includes("No+Images")
      ) {
        // *** Set referenceImageData with URL and default filters ***
        this.referenceImageData = {
          url: randomRefUrls[0],
          filters: { ...defaultFilters },
        };
      } else {
        // Handle case where no valid image was found
        this.referenceImageData = {
          url: PLACEHOLDER_REFERENCE_URL,
          filters: { ...defaultFilters },
        };
        console.warn(
          "Could not load initial reference image, using placeholder."
        );
      }
      // Initialize the top gallery with 8 image objects
      const galleryUrls = this.getRandomCaseImages(8);
      // *** Map URLs to objects with default filters ***
      this.galleryImages = galleryUrls.map((url) => {
        // Handle placeholder URLs from getRandomCaseImages if caseImageFiles was empty
        const isValidUrl = url && !url.includes("No+Images");
        return {
          url: isValidUrl ? url : PLACEHOLDER_DELETED_URL, // Use placeholder if needed
          filters: { ...defaultFilters },
        };
      });
      */
      // 只初始化為空或 placeholder
      this.referenceImageData = {
        url: PLACEHOLDER_REFERENCE_URL,
        filters: { ...defaultFilters },
      };
      this.galleryImages = Array(8).fill({
        url: '/img/cosmos/cosmos.jpg',
        filters: { ...defaultFilters },
      });
      this.generatedImages = [];

      console.log(
        "Initial loaded reference image data:",
        this.referenceImageData
      );
      console.log(
        "Initial loaded gallery images (objects):",
        this.galleryImages
      );
    },

    async fetchCategories() {
      try {
        // Using relative URL assuming API is served from the same origin in deployment,
        // or relying on proxy setup during development (vue.config.js).
        // Or use Amplify API if backend is managed by Amplify:
        // const response = await API.get('yourApiName', '/api/categories/');
        const response = await axios.get("/api/categories/"); // Adjusted URL
        console.log("Fetched categories:", response.data);
        // ... (rest of the category filtering logic remains the same) ...
        this.styles = response.data.filter((cat) => cat.type === "風格主題");
        this.materials = response.data.filter((cat) => cat.type === "框架材質");
        this.sidePanels = response.data.filter(
          (cat) => cat.type === "側板結構"
        );
        this.lighting = response.data.filter((cat) => cat.type === "光效樣式");
        this.interiors = response.data.filter((cat) => cat.type === "內部展示");
        this.designs = response.data.filter((cat) => cat.type === "整體設計");

        // Fallback static data remains useful if API fails
        if (!this.styles.length)
          this.styles = [
            { id: 1, name: "futuristic" },
            { id: 2, name: "minimalistic" },
            { id: 3, name: "industrial" },
            { id: 4, name: "cyberpunk" },
            { id: 5, name: "sci-fi" },
          ];
        if (!this.materials.length)
          this.materials = [
            { id: 1, name: "aluminum frame" },
            { id: 2, name: "steel-reinforced structure" },
            { id: 3, name: "titanium alloy" },
            { id: 4, name: "carbon fiber frame" },
            { id: 5, name: "lightweight magnesium frame" },
          ];
        if (!this.sidePanels.length)
          this.sidePanels = [
            { id: 1, name: "tempered glass side panel" },
            { id: 2, name: "full mesh panel" },
            { id: 3, name: "solid aluminum side panel" },
            { id: 4, name: "perforated steel panel" },
            { id: 5, name: "acrylic transparent panel" },
          ];
        if (!this.lighting.length)
          this.lighting = [
            { id: 1, name: "product photography lighting" },
            { id: 2, name: "natural sunlight" },
            { id: 3, name: "RGB studio lighting" },
            { id: 4, name: "ambient soft light" },
            { id: 5, name: "dark moody lighting" },
          ];
        if (!this.interiors.length)
          this.interiors = [
            { id: 1, name: "high-end internal components visible" },
            { id: 2, name: "RGB lighting system" },
            { id: 3, name: "custom water cooling loop" },
            { id: 4, name: "clean cable management" },
            { id: 5, name: "minimalist build" },
          ];
        if (!this.designs.length)
          this.designs = [
            { id: 1, name: "stylish and sleek industrial design" },
            { id: 2, name: "minimalist front panel with hidden ports" },
            { id: 3, name: "aggressive gaming aesthetic" },
            { id: 4, name: "symmetrical futuristic design" },
            { id: 5, name: "vertical front vent design" },
          ];
      } catch (error) {
        console.error("Error fetching categories, using static data:", error);
        // Static data fallback remains the same
        this.styles = [
          { id: 1, name: "futuristic" },
          { id: 2, name: "minimalistic" },
          { id: 3, name: "industrial" },
          { id: 4, name: "cyberpunk" },
          { id: 5, name: "sci-fi" },
        ];
        this.materials = [
          { id: 1, name: "aluminum frame" },
          { id: 2, name: "steel-reinforced structure" },
          { id: 3, name: "titanium alloy" },
          { id: 4, name: "carbon fiber frame" },
          { id: 5, name: "lightweight magnesium frame" },
        ];
        this.sidePanels = [
          { id: 1, name: "tempered glass side panel" },
          { id: 2, name: "full mesh panel" },
          { id: 3, name: "solid aluminum side panel" },
          { id: 4, name: "perforated steel panel" },
          { id: 5, name: "acrylic transparent panel" },
        ];
        this.lighting = [
          { id: 1, name: "product photography lighting" },
          { id: 2, name: "natural sunlight" },
          { id: 3, name: "RGB studio lighting" },
          { id: 4, name: "ambient soft light" },
          { id: 5, name: "dark moody lighting" },
        ];
        this.interiors = [
          { id: 1, name: "high-end internal components visible" },
          { id: 2, name: "RGB lighting system" },
          { id: 3, name: "custom water cooling loop" },
          { id: 4, name: "clean cable management" },
          { id: 5, name: "minimalist build" },
        ];
        this.designs = [
          { id: 1, name: "stylish and sleek industrial design" },
          { id: 2, name: "minimalist front panel with hidden ports" },
          { id: 3, name: "aggressive gaming aesthetic" },
          { id: 4, name: "symmetrical futuristic design" },
          { id: 5, name: "vertical front vent design" },
        ];
      }
    },
    // --- Update generateImage: New images in row 2 get current filters, old images moved to row 5 keep original filters ---
    async generateImage() {
      // --- 1. 收集 6 個 select 的值，如果是隨機則從列表中選擇一個 ---
      // 函數：從陣列中隨機選擇一個項目
      const getRandomOption = (options) => {
        if (!options || options.length === 0) return null;
        const randomIndex = Math.floor(Math.random() * options.length);
        return options[randomIndex];
      };

      // 函數：獲取選項的名稱（不是 ID）
      const getOptionName = (id, options) => {
        if (!id) return null; // 如果沒有選擇，返回 null
        const option = options.find(opt => opt.id === id);
        return option ? option.name : null;
      };

      // 對每個下拉選單，如果值為空（"隨機"），則隨機選一個，否則使用已選擇的
      const selections = {
        style: this.style ? getOptionName(this.style, this.styles) : getRandomOption(this.styles).name,
        chassis_frame: this.chassis_frame ? getOptionName(this.chassis_frame, this.materials) : getRandomOption(this.materials).name,
        side_type: this.side_type ? getOptionName(this.side_type, this.sidePanels) : getRandomOption(this.sidePanels).name,
        lighting_conditions: this.lighting_conditions ? getOptionName(this.lighting_conditions, this.lighting) : getRandomOption(this.lighting).name,
        interior_view: this.interior_view ? getOptionName(this.interior_view, this.interiors) : getRandomOption(this.interiors).name,
        front_layout: this.front_layout ? getOptionName(this.front_layout, this.designs) : getRandomOption(this.designs).name
      };

      console.log("最終選擇（包含隨機選中的值）:", selections);

      // --- 2. 處理原圖庫的圖片移動邏輯 ---
      // （保留原有邏輯）
      const galleryObjectsToMove = this.galleryImages.slice(0, 4);
      console.log("移動到生成區域的舊圖片物件:", galleryObjectsToMove);

      // 過濾掉任何無效的物件
      const validObjectsToMove = galleryObjectsToMove.filter(
        (obj) =>
          obj &&
          obj.url &&
          obj.url !== PLACEHOLDER_DELETED_URL &&
          !obj.url.startsWith("https://via.placeholder.com")
      );
      
      // 為新生成的圖片準備過濾器
      const currentFilters = {
        風格主題: selections.style,
        框架材質: selections.chassis_frame,
        側板結構: selections.side_type,
        光效樣式: selections.lighting_conditions,
        內部展示: selections.interior_view,
        整體設計: selections.front_layout
      };

      // 將有效的物件移至生成區域
      if (validObjectsToMove.length > 0) {
        this.generatedImages.unshift(...validObjectsToMove);
        console.log("已移動有效物件至生成區域:", this.generatedImages);
      }

      // --- 3. 調用 API 生成新圖片 ---
      try {
        this.isLoading = true;
        
        // 根據環境自動選擇 API 地址
        let baseUrl = getApiBaseUrl();
        
        console.log(`目前環境: ${window.location.hostname}, 使用 API 基礎網址: ${baseUrl}`);
        
        // --- 向 API 發送請求 ---
        const resp = await axios.post(`${baseUrl}/api/generate-images/`, {
          userSelections: selections, // 將選擇的值（而非 ID）發送至後端
          mask_mode: 0 // 添加 mask_mode 參數
        });

        // 處理 API 回傳的圖片 URL
        const fileUrls = resp.data.fileUrls;
        console.log("API 回傳的圖片 URLs:", fileUrls);

        if (Array.isArray(fileUrls) && fileUrls.length > 0) {
          // 創建新的畫廊物件，包含完整的圖片 URL 和目前的過濾器
          const newGalleryObjects = fileUrls.map(relativeUrl => {
            // 處理 URL：如果是相對路徑則加上基礎URL，如果是完整URL則直接使用
            let fullUrl = relativeUrl;
            if (relativeUrl && !relativeUrl.startsWith('http')) {
              fullUrl = baseUrl + relativeUrl.replace(/\\/g, '/');
            }
            return {
              url: fullUrl,
              filters: { ...currentFilters }
            };
          });

          // 更新畫廊的第一行
          this.galleryImages.splice(0, newGalleryObjects.length, ...newGalleryObjects);
          console.log("已更新畫廊的第一行:", this.galleryImages.slice(0, newGalleryObjects.length));
        } else {
          console.error("API 未返回預期的圖片 URL:", fileUrls);
          alert("生成成功，但未能獲取預期的圖片。請檢查後端日誌。");
        }
      } catch (err) {
        console.error("生成圖片時出錯:", err);
        this.error = err.response?.data?.error || err.message || "生成時發生未知錯誤";
        alert("生成圖片時出錯: " + this.error);
      } finally {
        this.isLoading = false;
      }
    },

    // Removed viewImage method as it depended on the old 'images' structure
    /*
    viewImage(image) {
      if (image && image.id) {
        this.$router.push({ name: 'image-detail', params: { id: image.id } });
      } else {
        console.warn("Attempted to view image with invalid data:", image);
      }
    }
    */

    // *** REVISED method for swapping reference object with gallery object ***
    swapReferenceWithGallery(clickedIndex) {
      if (clickedIndex < 0 || clickedIndex >= this.galleryImages.length) {
        return;
      }
      const clickedGalleryData = this.galleryImages[clickedIndex];
      const currentReferenceData = this.referenceImageData;

      // 檢查 gallery 圖片有效性
      if (
        !clickedGalleryData ||
        !clickedGalleryData.url ||
        clickedGalleryData.url === PLACEHOLDER_DELETED_URL ||
        clickedGalleryData.url.startsWith("https://via.placeholder.com")
      ) {
        return;
      }

      // 檢查 reference 圖片有效性
      const hasReference =
        currentReferenceData &&
        currentReferenceData.url &&
        currentReferenceData.url !== PLACEHOLDER_REFERENCE_URL;

      if (hasReference) {
        // 有圖則交換
        this.referenceImageData = clickedGalleryData;
        this.galleryImages.splice(clickedIndex, 1, currentReferenceData);
      } else {
        // 無圖則直接放到 reference，gallery 不變
        this.referenceImageData = clickedGalleryData;
      }
    },
    showInfo(source, data) {
      console.log(`showInfo called with source: ${source}, data:`, data);
      let imageDataToShow = null;
      try {
        if (source === "reference") {
          // Data is already the object (this.referenceImageData)
          if (
            data &&
            data.url &&
            !data.url.startsWith("https://via.placeholder.com") &&
            data.url !== PLACEHOLDER_REFERENCE_URL
          ) {
            imageDataToShow = data;
          } else {
            console.warn(
              "Attempted to show info for invalid or placeholder reference image."
            );
            alert("參考圖片無效或不存在。");
            return;
          }
        } else if (source === "gallery") {
          // *** MODIFIED: Data is now the index ***
          const index = data;
          if (index >= 0 && index < this.galleryImages.length) {
            const imgData = this.galleryImages[index]; // Get the object
            // Validate the object and its URL
            if (
              imgData &&
              imgData.url &&
              !imgData.url.startsWith("https://via.placeholder.com") &&
              imgData.url !== PLACEHOLDER_DELETED_URL
            ) {
              imageDataToShow = imgData; // Pass the whole object
            } else {
              console.log(
                "No info for placeholder/deleted gallery image object."
              );
              return;
            }
          } else {
            console.error(
              `Invalid index (${index}) for gallery images array (length: ${this.galleryImages.length}).`
            );
            alert("無效的圖庫索引。無法顯示資訊。");
            return;
          }
        } else if (source === "generated") {
          // Data is the index
          const index = data;
          if (index >= 0 && index < this.generatedImages.length) {
            const imgData = this.generatedImages[index]; // Get the object
            // Validate the object and its URL
            if (
              imgData &&
              imgData.url &&
              !imgData.url.startsWith("https://via.placeholder.com")
            ) {
              imageDataToShow = imgData; // Pass the whole object
            } else {
              console.warn(
                `Attempted to show info for invalid generated image data at index ${index}:`,
                imgData
              );
              alert(`索引 ${index} 處的生成圖片無效或數據不完整。`);
              return;
            }
          } else {
            console.error(
              `Invalid index (${index}) for generated images array (length: ${this.generatedImages.length}).`
            );
            alert("無效的生成圖片索引。無法顯示資訊。");
            return;
          }
        } else {
          console.error("Unknown source for showInfo:", source);
          alert("未知的圖片來源。");
          return;
        }

        // Show popup if we have valid data
        if (imageDataToShow) {
          console.log("Showing info for Image Data (object):", imageDataToShow);
          this.selectedImageDataForPopup = imageDataToShow;
          this.showPopup = true;
        } else {
          // This case should ideally be handled by the specific checks above
          console.warn("No valid image data found to show info for.");
        }
      } catch (error) {
        console.error("Error in showInfo:", error);
        alert("顯示圖片信息時發生錯誤。");
        this.showPopup = false;
        this.selectedImageDataForPopup = null;
      }
    },

    closeInfoPopup() {
      this.showPopup = false;
      this.selectedImageDataForPopup = null;
    },

    deleteImage(source, index) {
      try {
        if (source === "gallery") {
          if (index >= 0 && index < this.galleryImages.length) {
            console.log(
              `Replacing gallery image at index: ${index} with placeholder.`
            );
            this.galleryImages.splice(index, 1, {
              url: PLACEHOLDER_DELETED_URL,
              filters: null,
            });
            console.log("Updated gallery images:", this.galleryImages);
          } else {
            console.error(`Invalid index (${index}) for gallery delete.`);
            alert("無效的圖庫索引。");
          }
        } else if (source === "generated") {
          if (index >= 0 && index < this.generatedImages.length) {
            // *** MODIFIED: Log the object being deleted ***
            const deletedImageData = this.generatedImages[index];
            console.log(
              `Deleting generated image data at index: ${index}`,
              deletedImageData
            );
            this.generatedImages.splice(index, 1);
            console.log("Updated generated images:", this.generatedImages);
          } else {
            console.error(
              `Invalid index (${index}) for generated images delete.`
            );
            alert("無效的生成圖片索引。");
          }
        } else {
          console.error("Unknown source for deleteImage:", source);
          alert("未知的刪除來源。");
        }
      } catch (error) {
        console.error("Error in deleteImage:", error);
        alert("刪除圖片時發生錯誤。");
      }
    },

    clearUploadedImage() {
      console.log("Clearing uploaded image preview.");
      this.uploadedImagePreviewUrl = null;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = null;
      }
    },

    triggerFileUpload() {
      this.$refs.fileInput.click();
    },

    handleFileChange(event) {
      const files = event.target.files;
      if (!files.length) {
        console.log("No file selected.");
        return;
      }
      const file = files[0];

      // Basic validation (optional: size, type)
      if (!file.type.startsWith("image/")) {
        alert("請選擇圖片文件。");
        return;
      }

      console.log("Selected file:", file.name);

      // --- Preview Logic ---
      const reader = new FileReader();
      reader.onload = (e) => {
        this.uploadedImagePreviewUrl = e.target.result;
      };
      reader.onerror = (error) => {
        console.error("FileReader error:", error);
        alert("讀取文件時出錯。");
      };
      reader.readAsDataURL(file);

      // --- Backend Upload Logic ---
      // Now we uncomment and configure the axios call
      const formData = new FormData();
      // Ensure the key 'image' matches what the backend view expects (request.FILES['image'])
      formData.append("image", file);

      this.isLoading = true; // Show loading indicator

      // 根據環境自動選擇 API 地址
      let baseUrl = getApiBaseUrl();
      
      const uploadUrl = `${baseUrl}/api/upload/`;
      
      console.log(`正在上傳圖片到: ${uploadUrl}`);

      // Uncomment the actual upload call
      axios
        .post(uploadUrl, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("File uploaded successfully:", response.data);

          // Handle the response URL and possibly update the reference image
          if (response.data && response.data.fileUrl) {
            let fileUrl = response.data.fileUrl;
            // 如果返回的是相對路徑，添加基礎URL
            if (fileUrl && !fileUrl.startsWith('http')) {
              fileUrl = baseUrl + fileUrl;
            }

            // Create new reference image data with the uploaded image URL
            this.referenceImageData = {
              url: fileUrl,
              filters: {
                style: "隨機",
                material: "隨機",
                sidePanel: "隨機",
                lighting: "隨機",
                interior: "隨機",
                design: "隨機",
              },
            };

            console.log("Updated reference image:", this.referenceImageData);
          } else {
            console.error("Unexpected response format:", response.data);
            alert("上傳成功但回傳格式異常。");
          }
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
          alert("上傳文件時出錯：" + (error.response?.data?.error || error.message));
        })
        .finally(() => {
          this.isLoading = false; // Hide loading indicator
        });
    },
    swapReferenceWithGenerated(index) {
      console.log(`Attempting swap for generated image at index: ${index}`);
      if (index < 0 || index >= this.generatedImages.length) {
        console.error(`Invalid index (${index}) for swapping.`);
        alert("無效的生成圖片索引。");
        return;
      }
      const generatedImageData = this.generatedImages[index];
      const currentReferenceData = this.referenceImageData;
      if (
        !generatedImageData ||
        !generatedImageData.url ||
        generatedImageData.url.startsWith("https://via.placeholder.com")
      ) {
        console.warn(
          `Attempted to swap with invalid generated image data at index ${index}:`,
          generatedImageData
        );
        alert("無法選擇無效的生成圖片進行交換。");
        return;
      }
      if (
        !currentReferenceData ||
        !currentReferenceData.url ||
        currentReferenceData.url === PLACEHOLDER_REFERENCE_URL
      ) {
        console.warn(
          "Attempted to swap from an invalid reference image:",
          currentReferenceData
        );
        alert("參考圖片無效，無法進行交換。請先選擇有效的參考圖片。");
        return;
      }
      console.log(
        `Swapping reference (${JSON.stringify(
          currentReferenceData
        )}) with generated index ${index} (${JSON.stringify(
          generatedImageData
        )})`
      );
      this.referenceImageData = generatedImageData;
      this.generatedImages.splice(index, 1, currentReferenceData);
      console.log(
        "Swap complete. New referenceImageData:",
        this.referenceImageData
      );
      console.log("Updated generatedImages:", this.generatedImages);
    },
    getSelectedName(id, options) {
      if (!id) return "隨機";
      const found = Array.isArray(options)
        ? options.find((opt) => opt.id === id)
        : null;
      return found ? found.name : "隨機";
    },
    handleMenuClick(index) {
      this.activeMenuItem = index;
      if (this.menuItems[index] === "儲存的專案") {
        this.$router.push("/saved");
      }
    },
  },
  watch: {
    galleryImages: {
      handler(newVal) {
        // 保持 isFavoriteGallery 長度與 galleryImages 一致
        this.isFavoriteGallery = newVal.map(
          (_, i) => this.isFavoriteGallery[i] || false
        );
      },
      immediate: true,
      deep: true,
    },
  },
};
</script>

<style scoped>
.home-container {
  display: flex;
  background-color: #000;
  color: #fff;
  min-height: calc(100vh - 4rem);
  padding-top: 1rem;
}

.sidebar {
  width: 200px;
  background-color: #21005d;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-section {
  margin-bottom: 2rem;
}

.sidebar-title {
  font-size: 0.9rem;
  font-weight: normal;
  color: #ccc;
  margin-bottom: 0.8rem;
}

.number-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
}

.number-buttons button {
  background-color: #3a2a5b;
  color: #ccc;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.2s;
}

.number-buttons button:hover {
  background-color: #4a3a6b;
}

.number-buttons button.active {
  background-color: #eee;
  color: #21005d;
  font-weight: bold;
}

.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu li {
  padding: 0.8rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #ccc;
  font-size: 0.9rem;
}

.menu li:hover {
  background-color: #3a2a5b;
}

.menu li.active {
  background-color: #eee;
  color: #21005d;
  font-weight: bold;
}

.content-area {
  flex-grow: 1;
  padding: 0 2rem 2rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 100vw;
  overflow-x: auto;
  box-sizing: border-box;
}

.content-row {
  display: grid;
  gap: 1.5rem;
}

.top-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 2rem;
  justify-content: center;
  align-items: stretch;
}

.gallery-row {
  grid-template-columns: repeat(4, 1fr);
}

.filters-row {
  grid-template-columns: repeat(3, 1fr);
  align-items: end;
}

.button-row {
  display: flex;
  justify-content: center;
}

.content-box {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 150px;
  min-width: 0;
  box-sizing: border-box;
}

.image-box {
  padding: 0.5rem;
  background-color: #444;
  overflow: hidden;
}

.image-box img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
}

.reference-box {
  position: relative;
  /* Needed for absolute positioning of actions */
  gap: 0.5rem;
  aspect-ratio: 4 / 3;
}

.reference-box img {
  /* These might force stretching if container size is fixed 
  height: 100%; 
  width: 100%; 
  */
  /* object-fit: cover; Remove this to inherit object-fit: contain from .image-box img */
}

.gallery-item {
  position: relative;
  /* Needed for absolute positioning of actions */
  aspect-ratio: 4 / 3;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.gallery-item:hover {
  transform: scale(1.03);
}

.gallery-item img {
  /* These might force stretching if container size is fixed 
  width: 100%;
  height: 100%;
  */
  /* object-fit: cover; Remove this to inherit object-fit: contain from .image-box img */
}

.upload-box {
  position: relative;
  /* Needed for absolute positioning of actions */
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Default state styles */
  flex-direction: column;
  gap: 0.5rem;
  color: #aaa;
  border: 2px dashed #555;
  background-color: #333;
  aspect-ratio: 4 / 3;
}

.upload-box:hover {
  background-color: #404040;
  border-color: #777;
}

.upload-icon {
  width: 24px;
  height: 24px;
  stroke: #aaa;
}

.uploaded-preview-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  /* Keep aspect ratio */
  border-radius: 8px;
  /* Match other image boxes */
}

/* Styles for buttons on top of the preview */
.upload-box .image-actions {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  display: flex;
  gap: 0.4rem;
  z-index: 10;
}

.upload-replace-btn {
  /* Inherits .action-btn styles */
  /* Optional: different background? */
  background-color: rgba(60, 60, 150, 0.8);
}

.upload-replace-btn:hover {
  background-color: rgba(80, 80, 180, 0.9);
}

.replace-upload-icon {
  width: 14px;
  /* Smaller icon for the button */
  height: 14px;
  stroke: white;
  stroke-width: 2;
  /* Make stroke slightly bolder */
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: #ccc;
  align-items: stretch;
}

.filter-group label {
  font-size: 0.9rem;
  text-align: left;
  margin-left: 0.5rem;
}

.filter-group select {
  background-color: #eee;
  color: #333;
  border: none;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke-width='2' stroke='%23333' class='w-6 h-6'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='m19.5 8.25-7.5 7.5-7.5-7.5' /%3E%3C/svg%3E%0A");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1em;
  cursor: pointer;
  width: 100%;
}

.generate-btn {
  background-color: #4a0d7a;
  color: white;
  border: none;
  padding: 0.8rem 2.5rem;
  border-radius: 20px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  font-weight: bold;
}

.generate-btn:hover {
  background-color: #6a1d9a;
}

/* Add styles for loading state if needed */
.image-box span {
  color: #888;
  font-size: 0.9em;
}

/* Style for the gallery title */
.gallery-title {
  font-size: 0.9rem;
  /* Match filter labels */
  font-weight: normal;
  /* Match sidebar title */
  color: #ccc;
  /* Match sidebar title */
  text-align: left;
  /* margin-bottom: 0.8rem; /* Match sidebar title */
  margin-bottom: 0.3rem;
  /* Reduced bottom margin */
  /* margin-left: 0.5rem; /* Optional: Match filter labels left margin if needed */
}

/* Styles for the VERTICAL generated gallery container (now grid) */
.generated-gallery-container {
  /* display: block; Change back to grid */
  display: grid;
  /* Use grid for 4 columns */
  grid-template-columns: repeat(4, 1fr);
  /* Define 4 equal columns */
  gap: 1.5rem;
  /* Add gap between grid items */
  overflow-y: auto;
  /* Enable vertical scroll */
  padding: 1rem;
  border: 1px solid #555;
  border-radius: 8px;
  background-color: #303030;
  max-height: 400px;
  /* Keep max height for vertical scroll */
  /* Scrollbar styling remains the same */
  scrollbar-width: thin;
  scrollbar-color: #666 #303030;
}

.generated-gallery-container::-webkit-scrollbar {
  width: 8px;
  /* Width of the scrollbar */
}

.generated-gallery-container::-webkit-scrollbar-track {
  background: #303030;
  /* Track color */
  border-radius: 4px;
}

.generated-gallery-container::-webkit-scrollbar-thumb {
  background-color: #666;
  /* Thumb color */
  border-radius: 4px;
  border: 2px solid #303030;
  /* Padding around thumb */
}

/* Styles for items specifically INSIDE the generated container */
.generated-gallery-container .gallery-item {
  /* width: 100%; Remove width, grid handles it */
  /* margin-bottom: 1.5rem; Remove margin, gap handles it */
  /* Aspect ratio is inherited from .gallery-item */
  cursor: pointer;
}

/* REMOVE last item margin adjustment as grid gap handles spacing */
/*
.generated-gallery-container .gallery-item:last-child {
    margin-bottom: 0;
}
*/

/* Optional: Style for the empty gallery message */
.empty-gallery-message {
  color: #888;
  font-style: italic;
  text-align: center;
  width: 100%;
  /* Take full width if container is empty */
  padding: 2rem 0;
}

.image-actions {
  position: absolute;
  top: 0.5rem;
  /* Adjust as needed */
  right: 0.5rem;
  /* Adjust as needed */
  display: flex;
  gap: 0.4rem;
  z-index: 10;
  /* Ensure buttons are clickable */
}

.action-btn {
  background-color: rgba(40, 40, 40, 0.8);
  /* Semi-transparent background */
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  /* Make them circular */
  width: 24px;
  /* Fixed size */
  height: 24px;
  /* Fixed size */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  transition: background-color 0.2s, border-color 0.2s;
}

.action-btn:hover {
  background-color: rgba(70, 70, 70, 0.9);
  border-color: rgba(255, 255, 255, 0.8);
}

.info-btn {
  /* Optional: specific color */
  /* background-color: rgba(0, 100, 200, 0.8); */
}

.delete-btn {
  /* Optional: specific color */
  background-color: rgba(200, 50, 50, 0.8);
}

.delete-btn:hover {
  background-color: rgba(230, 70, 70, 0.9);
}

.param-box {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直置中 */
  align-items: flex-start;
  height: 100%;
}
.param-title {
  margin-bottom: 1rem;
  align-self: flex-start;
}
.param-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center; /* 水平置中 ul */
  flex: 1;
}
.param-content ul {
  width: auto;
  margin: 0 auto;
  text-align: left;
  padding-left: 0;
  list-style: none;
  word-break: break-all;
  font-size: 1.15em;
  color: #fff;
}
.param-content li {
  margin-bottom: 0.3rem;
  width: 100%;
  white-space: normal;
  overflow-wrap: anywhere;
}

@media (max-width: 1200px) {
  .top-row {
    gap: 1rem;
  }
}
@media (max-width: 900px) {
  .home-container {
    flex-direction: column;
    padding: 0.5rem;
  }
  .sidebar {
    width: 100%;
    flex-direction: row;
    padding: 1rem 0.5rem;
  }
  .content-area {
    padding: 0 0.5rem 1rem 0.5rem;
  }
  .top-row {
    grid-template-columns: 1fr;
  }
  .gallery-row,
  .filters-row,
  .generated-gallery-container {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 600px) {
  .sidebar {
    font-size: 0.95em;
    padding: 0.5rem 0.2rem;
  }
  .top-row,
  .gallery-row,
  .filters-row,
  .generated-gallery-container {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  .content-box {
    min-height: 100px;
    padding: 0.5rem;
  }
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
  /* stroke: #fff; <- Removed, stroke is defined in SVG now */
  /* fill: none; <- Removed, fill is defined in SVG now */
  transition: fill 0.2s, stroke 0.2s; /* Added stroke transition */
}
.favorite-btn.favorited svg {
  fill: #e24a7a; /* Keep fill color */
  stroke: #e24a7a; /* Add stroke color for consistency */
}
</style>
 