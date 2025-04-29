<template>
  <div class="image-detail" v-if="image">
    <div class="image-container">
      <img :src="getImageUrl(image.image)" :alt="image.title">
    </div>
    
    <div class="image-info">
      <h1>{{ image.title }}</h1>
      <p class="category">分類：{{ categoryName }}</p>
      <p class="description">{{ image.description }}</p>
      <p class="date">上傳日期：{{ formatDate(image.created_at) }}</p>
      
      <button @click="goBack">返回</button>
    </div>
  </div>
  <div v-else class="loading">
    <p>載入中...</p>
  </div>
</template>

<script>
import axios from 'axios'

// 工具函數：根據當前環境返回正確的API基礎URL
function getApiBaseUrl() {
  // 檢查當前域名判斷環境
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // 本地開發環境
    return 'http://localhost:8080';
  } else {
    // 生產環境使用 Elastic Beanstalk URL
    return 'https://hackathon-backend-env.eba-z3mtvcpp.us-east-1.elasticbeanstalk.com';
  }
}

export default {
  name: 'ImageDetailView',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      image: null,
      category: null,
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchImage()
  },
  computed: {
    categoryName() {
      return this.category ? this.category.name : ''
    }
  },
  methods: {
    async fetchImage() {
      try {
        this.loading = true
        const baseUrl = getApiBaseUrl();
        const response = await axios.get(`${baseUrl}/api/images/${this.id}/`)
        this.image = response.data
        
        if (this.image.category) {
          const categoryResponse = await axios.get(`${baseUrl}/api/categories/${this.image.category}/`)
          this.category = categoryResponse.data
        }
        
        // 如果圖片URL是相對路徑，添加基礎URL
        if (this.image && this.image.image && !this.image.image.startsWith('http')) {
          this.image.imageUrl = baseUrl + this.image.image
        }
        
        this.loading = false
      } catch (error) {
        console.error('Error fetching image', error)
        this.error = 'Could not load image data'
        this.loading = false
      }
    },
    getImageUrl(imageUrl) {
      if (!imageUrl) return '';
      const baseUrl = getApiBaseUrl();
      return imageUrl.startsWith('http') ? imageUrl : baseUrl + imageUrl;
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('zh-TW', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    },
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped>
.image-detail {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  margin-top: 1rem;
}

.image-container {
  flex: 3;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.image-container img {
  width: 100%;
  height: auto;
  display: block;
}

.image-info {
  flex: 2;
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-top: 0;
  color: #2c3e50;
}

.category {
  background-color: #3498db;
  color: white;
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.description {
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.date {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #2980b9;
}

.loading {
  text-align: center;
  padding: 3rem;
}

@media (max-width: 768px) {
  .image-detail {
    flex-direction: column;
  }
  
  .image-container, .image-info {
    width: 100%;
  }
}
</style> 