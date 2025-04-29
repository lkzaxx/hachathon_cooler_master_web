module.exports = {
    root: true,
    env: {
        node: true,
    },
    extends: [
        "plugin:vue/vue3-essential", // 使用 Vue 3 的基本規則
        "eslint:recommended", // 使用 ESLint 推薦的基本規則
    ],
    parserOptions: {
        parser: "@babel/eslint-parser", // 指定解析器
        requireConfigFile: false // 如果沒有 Babel 配置，需要這個
    },
    rules: {
        // 在這裡可以自定義或覆蓋規則
        // 例如：關閉未使用變數的警告 (不建議長期關閉)
        // 'no-unused-vars': 'off',
        'vue/multi-word-component-names': 'off', // 允許單詞組件名，如 HomeView.vue
    },
}; 