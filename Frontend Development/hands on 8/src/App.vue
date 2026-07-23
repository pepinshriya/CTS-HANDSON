<template>
  <div>
    <nav>
      <RouterLink to="/">Home</RouterLink>

      <RouterLink to="/courses">
        Courses
      </RouterLink>

      <RouterLink to="/profile">
        Profile
      </RouterLink>
    </nav>

    <RouterView />
  </div>
</template>

<script setup>
// No JavaScript is required for this step.
</script>

<style scoped>
nav {
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: #42b883;
}

nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

nav a.router-link-active {
  text-decoration: underline;
}
</style>