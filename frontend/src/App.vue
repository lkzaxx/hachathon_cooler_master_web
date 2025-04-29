<template>
  <div id="app">
    <header>
      <nav>
        <div class="logo">
          <router-link to="/">
            <img src="/img/logo.png" alt="Logo" class="header-logo">
          </router-link>
        </div>
      </nav>
    </header>

    <main>
      <router-view />
    </main>

    <footer>
      <p>&copy; cooler master case generator</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Microsoft JhengHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background-color: #21005D;
  color: white;
  padding: 1rem;
}

nav {
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo a {
  text-decoration: none;
  display: inline-block;
  line-height: 0;
}

.header-logo {
  height: 40px;
  width: auto;
  vertical-align: middle;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  background-color: #34495e;
}

main {
  flex: 1;
  width: 100%;
}

footer {
  background-color: #21005D;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
</style>