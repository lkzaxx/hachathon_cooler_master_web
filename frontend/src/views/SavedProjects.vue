<template>
  <div class="home-container">
    <aside class="sidebar">
      <nav class="menu">
        <ul>
          <li v-for="(item, index) in menuItems" :key="index" :class="{ active: activeMenuItem === index }"
              @click="handleMenuClick(index)">
            {{ item }}
          </li>
        </ul>
      </nav>
    </aside>
    <main class="content-area">
      <h2 class="favorites-title">我的最愛機殼</h2>
      <div class="gallery-wrapper">
        <div class="content-row gallery-row">
          <div v-for="(img, i) in favoriteImages" :key="i" class="content-box image-box gallery-item" @click="showSavedItemInfo(i)">
            <img :src="img" alt="favorite case" />
            <button
              v-if="img"
              class="favorite-btn"
              :class="{ favorited: isFavoriteSaved[i] }"
              @click.stop="isFavoriteSaved[i] = !isFavoriteSaved[i]"
              style="position:absolute; right:0.8rem; bottom:0.8rem;"
            >
              <svg v-if="!isFavoriteSaved[i]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.218l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div class="back-button-container">
        <button class="back-btn" @click="goBack">返回</button>
      </div>
    </main>

    <!-- Saved Item Info Popup -->
    <saved-item-info-popup
      :is-visible="showSavedPopup"
      :image-data="selectedSavedItemData"
      @close="closeSavedPopup"
    />
  </div>
</template>

<script>
import SavedItemInfoPopup from '@/components/SavedItemInfoPopup.vue';

export default {
  name: 'SavedProjects',
  components: {
    SavedItemInfoPopup
  },
  data() {
    return {
      menuItems: [
        '專案一 Cosmos',
        '專案二 MasterBox',
        '專案三 Cube',
        '專案四 NR200NX',
        '專案五 CubeBox',
        '專案六 New Comos',
        '儲存的專案',
      ],
      activeMenuItem: 6,
      favoriteImages: [
        '/img/Computer_Case/ComfyUI_00003__0.png',
        '/img/Computer_Case/ComfyUI_00004__0.png',
        '/img/Computer_Case/ComfyUI_00006__0.png',
        '/img/Computer_Case/ame.png',
        '/img/Computer_Case/bae.png',
        '/img/Computer_Case/aqua.png',
        '/img/Computer_Case/mori.png',
        '/img/Computer_Case/kronii.png',
        '/img/Computer_Case/ComfyUI_00003__0.png',
        '/img/Computer_Case/ComfyUI_00004__0.png',
        '/img/Computer_Case/ComfyUI_00006__0.png',
        '/img/Computer_Case/ame.png',
      ],
      isFavoriteSaved: [],
      showSavedPopup: false,
      selectedSavedItemData: null
    }
  },
  mounted() {
    this.isFavoriteSaved = this.favoriteImages.map(() => false);
  },
  methods: {
    handleMenuClick(index) {
      this.activeMenuItem = index;
      if (this.menuItems[index] === '儲存的專案') {
        if (this.$route.path !== '/saved') {
          this.$router.push('/saved');
        }
      } else if (index === 0) {
        this.$router.push('/');
      } else {
        this.$router.push('/');
      }
    },
    goBack() {
      this.$router.back();
    },
    showSavedItemInfo(index) {
      const dataToShow = {
        url: this.favoriteImages[index],
        prompt: `This is a placeholder prompt for image ${index + 1}. A futuristic premium PC case inspired by Cooler Master Cosmos, aluminum frame, tempered glass side panel, glowing purple RGB lighting, high-end internal components visible.`,
        filters: {
          material: '鋁合金',
          sidePanel: '鋼化玻璃',
          lighting: '紫色RGB',
          interior: '可見',
          design: '未來感'
        }
      };
      console.log('Showing info for:', dataToShow);
      this.selectedSavedItemData = dataToShow;
      this.showSavedPopup = true;
    },
    closeSavedPopup() {
      this.showSavedPopup = false;
      this.selectedSavedItemData = null;
    }
  }
}
</script>

<style scoped>
/* Layout and Sidebar Styles (Copied from HomeView) */
.home-container {
  display: flex;
  background-color: #000;
  color: #fff;
  min-height: calc(100vh - 92px); /* Adjust based on App.vue header/footer height */
  padding-top: 1rem;
}
.sidebar {
  width: 200px;
  background-color: #21005D;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
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
  color: #21005D;
  font-weight: bold;
}
/* Main Content Area Styles (Copied from HomeView) */
.content-area {
  flex-grow: 1;
  padding: 1.5rem 2rem 3rem 2rem; /* Increased top/bottom padding */
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 100vw;
  overflow-x: auto;
  box-sizing: border-box;
}
/* Gallery Wrapper for Centering and Width Constraint */
.gallery-wrapper {
  max-width: 80%; /* Constrain width */
  margin: 1rem auto; /* Vertical margin and horizontal centering */
  width: 100%; /* Ensure it takes space for centering */
}
/* Gallery Grid (4 columns) */
.content-row.gallery-row {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(4, 1fr); /* Kept at 4 columns */
}
.content-box {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Removed min-height to allow natural sizing */
  min-width: 0;
  box-sizing: border-box;
  position: relative;
}
.image-box {
  background-color: #444;
  overflow: hidden;
}
.image-box img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
  border-radius: 8px;
  width: 100%;
  height: 100%;
}
.gallery-item {
  aspect-ratio: 1 / 1;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  border: 3px solid transparent;
}
.gallery-item:hover {
  transform: scale(1.03);
}
/* Title Style */
.favorites-title {
  color: #fff;
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 0.5rem; /* Reduced margin */
  text-align: left;
  padding-left: 10%; /* Align roughly with constrained gallery */
}
/* Favorite Button Style (Copied from HomeView/Popup) */
.favorite-btn {
  position: absolute;
  right: 0.8rem;
  bottom: 0.8rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 2;
}
.favorite-btn svg {
  width: 24px; /* Slightly smaller */
  height: 24px;
  transition: fill 0.2s, stroke 0.2s;
}
.favorite-btn.favorited svg {
  fill: #e24a7a;
  stroke: #e24a7a;
}
/* Back Button Styles */
.back-button-container {
  text-align: center;
  margin-top: 2rem; /* Space above the button */
}
.back-btn {
  background: #f5e6f7;
  color: #333;
  border: none;
  border-radius: 10px;
  padding: 0.7em 2.2em;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
.back-btn:hover {
  background: #e0c6f0;
}
/* Responsive (Copied/Adjusted from HomeView) */
@media (max-width: 1200px) {
  .gallery-wrapper {
    max-width: 90%; /* Slightly wider on medium screens */
  }
  .content-row.gallery-row {
    grid-template-columns: repeat(3, 1fr); /* 3 columns */
  }
  .favorites-title {
     padding-left: 5%;
  }
}
@media (max-width: 900px) {
  .home-container {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
    flex-direction: row;
    padding: 0.5rem 1rem; /* Adjust padding */
    justify-content: center; /* Center items */
  }
  .menu ul {
    display: flex;
    flex-wrap: wrap; /* Allow wrapping */
    justify-content: center;
  }
  .menu li {
    margin-bottom: 0.3rem;
    margin-right: 0.3rem; /* Add horizontal gap */
  }
  .content-area {
     padding: 1rem;
  }
   .gallery-wrapper {
    max-width: 100%; /* Full width on smaller screens */
    margin: 1rem auto;
  }
  .content-row.gallery-row {
    grid-template-columns: repeat(2, 1fr); /* 2 columns */
  }
  .favorites-title {
     padding-left: 0;
     text-align: center; /* Center title */
  }
}
@media (max-width: 600px) {
  .content-row.gallery-row {
    grid-template-columns: 1fr; /* 1 column */
    gap: 1rem; /* Reduce gap */
  }
  .gallery-item {
    aspect-ratio: 4 / 3; /* Adjust aspect ratio if needed */
  }
  .favorites-title {
     font-size: 1.4rem;
  }
  .back-btn {
    font-size: 1rem;
    padding: 0.6em 1.8em;
  }
}
</style> 