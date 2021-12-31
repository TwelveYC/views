<template>
    <div class="container">
        <div class="controlBox">
            <el-form ref="form" :model="form" label-width="80px">
                <el-form-item label="节点数目">
                    <el-input-number v-model="form.n"></el-input-number>
                </el-form-item>
                <el-form-item label="新增边数">
                    <el-input-number v-model="form.m"></el-input-number>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onSubmit">确认</el-button>
                </el-form-item>
                <el-form-item label="当前网络">
                    <el-input-number v-model="evoState.ii" @change="indexChange" :min="0" :max="evoState.ii_length"></el-input-number>
                </el-form-item>
            </el-form>
        </div>
        <div ref="mainsvg" class="mainsvg"></div>
    </div>
</template>

<script>
    import axios from 'axios';
    import * as echarts from 'echarts';
    export default {
        name: "evolutionNetworks",
        mounted() {
            this.charts = echarts.init(this.$refs.mainsvg);
        },
        data() {
            return {
                form: {
                    n: 100,
                    m: 2
                },
                evolutionNetwortkUrl: "http://10.154.51.137:8000/nets/evolution/",
                graphs: [],
                charts: null,
                evoState: {
                    ii: 0,
                    ii_length : 0
                }
            }
        },
        methods: {
            onSubmit() {
                axios.get(this.evolutionNetwortkUrl, {
                    params: {
                        n: this.form.n,
                        m: this.form.m,
                    }
                }).then(res => {
                    this.graphs.push(...res.data.data);
                    this.evoState.ii_length = res.data.data.length;
                })
            },
            indexChange(n) {
                const options = {
                    series: [{
                        type: "graph",
                        data: this.graphs[n].nodes,
                        links: this.graphs[n].links,
                        layout: "circular",
                    }]
                };
                this.charts.setOption(options);
            }
        }
    }
</script>

<style scoped>
    .container{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: row;
    }

    .mainsvg{
        height: 100%;
        width: 70%;
    }

    .controlBox{
        height: 100%;
        width: 30%;
    }

</style>