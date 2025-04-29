import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CategoryView from '../views/CategoryView.vue'
import ImageDetailView from '../views/ImageDetailView.vue'
import SavedProjects from '../views/SavedProjects.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/categories',
        name: 'categories',
        component: CategoryView
    },
    {
        path: '/image/:id',
        name: 'image-detail',
        component: ImageDetailView,
        props: true
    },
    {
        path: '/saved',
        name: 'saved-projects',
        component: SavedProjects
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router 