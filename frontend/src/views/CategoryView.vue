<template>
  <div class="categories">
    <h1>圖片分類</h1>
    
    <div class="category-list">
      <div v-for="category in categories" :key="category.id" class="category-card">
        <h2>{{ category.name }}</h2>
        <p>{{ category.description }}</p>
        <div class="category-images">
          <div v-for="image in category.images.slice(0, 3)" :key="image.id" class="category-image">
            <img :src="getImageUrl(image.image)" :alt="image.title">
          </div>
        </div>
        <button @click="viewCategory(category)">查看所有圖片</button>
      </div>
    </div>
    
    <div v-if="selectedCategory" class="category-details">
      <h2>{{ selectedCategory.name }}</h2>
      <div class="image-gallery">
        <div v-for="image in selectedCategory.images" :key="image.id" class="image-card" @click="viewImage(image)">
          <img :src="getImageUrl(image.image)" :alt="image.title">
          <h3>{{ image.title }}</h3>
        </div>
      </div>
    </div>
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
  name: 'CategoryView',
  data() {
    return {
      categories: [],
      selectedCategory: null
    }
  },
  created() {
    this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      try {
        const baseUrl = getApiBaseUrl();
        const response = await axios.get(`${baseUrl}/api/categories/`)
        this.categories = response.data
      } catch (error) {
        console.error('Error fetching categories', error)
      }
    },
    getImageUrl(imageUrl) {
      const baseUrl = getApiBaseUrl();
      return baseUrl + imageUrl
    },
    viewCategory(category) {
      this.selectedCategory = category
    },
    viewImage(image) {
      this.$router.push({ name: 'image-detail', params: { id: image.id } })
    }
  }
}
</script>

<style scoped>
.categories {
  text-align: center;
}

h1 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.category-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.category-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.category-card h2 {
  color: #2c3e50;
  margin-top: 0;
}

.category-images {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
}

.category-image {
  flex: 1;
  height: 100px;
  overflow: hidden;
  border-radius: 4px;
}

.category-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #2980b9;
}

.category-details {
  margin-top: 3rem;
  border-top: 1px solid #eee;
  padding-top: 2rem;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.image-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  cursor: pointer;
}

.image-card:hover {
  transform: translateY(-5px);
}

.image-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.image-card h3 {
  padding: 1rem;
  margin: 0;
  font-size: 1rem;
}
</style> 