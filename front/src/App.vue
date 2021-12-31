<template>
  <div id="app">
    <el-container>
      <el-header>
        <router-link to="/sf">Nets</router-link> |
        <router-link to="/ev">Evolution Network</router-link>|
        <router-link to="/map">道路网络</router-link>
      </el-header>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<style>
  html{
    width: 100%;
    height: 100%;
  }

  body{
    width: 100%;
    height: 100%;
    margin: 0;
  }

  #app {
    width: 100%;
    height: 100%;
  }


  .el-container {
    height: 100%;
  }
  .el-main{
    height: 100%;
  }

  .el-header{
    display: flex;
    flex-direction: row;
    justify-content: space-evenly
  }

</style>
