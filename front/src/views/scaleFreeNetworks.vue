<template>

<div class="container">
    <div class="controlBox">
        <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="网络类型">
                <el-select v-model="form.networkType" placeholder="网络类型">
                    <el-option label="无标度网络" value="sf"></el-option>
                    <el-option label="小世界网络" value="sw"></el-option>
                    <el-option label="随机网络" value="random"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="节点数目">
                <el-form-item placeholder="节点数目">
                    <el-input-number v-model="form.n"></el-input-number>
                </el-form-item>
            </el-form-item>
            <el-form-item v-for="(item, index) in is_show" :key="index" v-show="item" :label="form.parameters[index].name">
                <el-input-number v-model="form.parameters[index].v"> </el-input-number>
            </el-form-item>
            <el-form-item label="布局方式">
                <el-radio-group v-model="form.layout">
                    <el-radio label="circular" value="circular"></el-radio>
                    <el-radio label="force" value="force"></el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item label="斥力因子" v-show="form.layout === 'force'">
                <el-input-number v-model="form.forceParameter.repulsion"> </el-input-number>
            </el-form-item>
            <el-form-item label="引力因子" v-show="form.layout === 'force'">
                <el-input-number v-model="form.forceParameter.gravity"> </el-input-number>
            </el-form-item>
            <el-form-item label="边长度" v-show="form.layout === 'force'">
                <el-input-number v-model="form.forceParameter.edgeLength"> </el-input-number>
            </el-form-item>

            <el-form-item label="映射方式">
                <el-radio-group v-model="form.mapType">
                    <el-radio label="none"></el-radio>
                    <el-radio label="color"></el-radio>
                </el-radio-group>
            </el-form-item>

            <el-form-item v-show="form.mapType !== 'none'" label="映射属性">
                <el-select v-model="form.mapAttr" >
                    <el-option v-for="(item, index) in mapAttrs" :label="item" :value="item"></el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="节点尺寸" v-show="form.mapType === 'none'">
                <el-input-number v-model="form.nodeSize"> </el-input-number>
            </el-form-item>

            <el-form-item label="节点颜色" v-show="form.mapType === 'none'">
                <el-color-picker v-model="form.nodeColor"> </el-color-picker>
            </el-form-item>

            <el-form-item label="连边宽度" v-show="form.mapType === 'none'">
                <el-input-number v-model="form.edgeWith"> </el-input-number>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="onSubmit">立即创建</el-button>
            </el-form-item>
        </el-form>
    </div>
    <div ref="mainsvg" class="mainsvg"></div>
</div>

</template>

<script>
    import axios from 'axios';
    import * as echarts from 'echarts';
    import * as d3 from "d3";
    export default {
        name: "scaleFreeNetworks",
        mounted() {
            this.charts = echarts.init(this.$refs.mainsvg);
        },
        methods: {
            draw() {
                const options = {
                    series: [{
                        type: "graph",
                        data: this.networkData.nodes,
                        links: this.networkData.links,
                        layout: this.form.layout,
                    }]
                }
                if(this.form.layout === "force") {
                    options.series[0].force = this.form.forceParameter;
                }

                if (this.form.mapType !== "none") {
                    const data = this.networkData.nodes.map(v => v[this.form.mapAttr]);
                    if(this.form.mapType === "color") {
                        const mapScale = d3.scaleSequential(d3.interpolateRdYlGn);
                        mapScale.domain(d3.extent(data));
                        options.series[0].itemStyle = {
                            color: obj => {
                                return mapScale(obj.data[this.form.mapAttr])
                            }
                        };

                    }
                }else {
                    options.series[0].symbolSize = this.form.nodeSize;
                    options.series[0].itemStyle = {
                        color: this.form.nodeColor
                    };
                    options.series[0].lineStyle = {
                        width : this.form.edgeWith
                    };
                }

                this.charts.setOption(options);
            },
            onSubmit() {
                if(this.form.networkType === "sf") {
                    axios.get(this.scaleFreeNetworksUrl, {
                        params: {
                            n: this.form.n,
                            m: this.form.parameters[0].v
                        }
                    }).then(res => {
                        this.networkData = res.data.data;
                        this.draw();
                    })

                }else if(this.form.networkType === "sw") {
                    axios.get(this.smallWorldNetworksUrl, {
                        params: {
                            n: this.form.n,
                            k: this.form.parameters[1].v,
                            p: this.form.parameters[2].v
                        }
                    }).then(res => {
                        this.networkData = res.data.data;
                        this.draw();
                    })

                }else if (this.form.networkType === "random") {
                    axios.get(this.randomNetworksUrl, {
                        params: {
                            n: this.form.n,
                            p: this.form.parameters[3].v
                        }
                    }).then(res => {
                        this.networkData = res.data.data;
                        this.draw();
                    })

                }
            }
        },
        data() {
            return {
                scaleFreeNetworksUrl: "http://10.154.51.137:8000/nets/sf/",
                smallWorldNetworksUrl: "http://10.154.51.137:8000/nets/sw/",
                randomNetworksUrl: "http://10.154.51.137:8000/nets/random/",
                networkData: null,
                charts: null,
                form: {
                    networkType: 'sf',
                    n: 100,
                    parameters: [{v: 2, name: "sf_m"}, {v: 2, name:"sw_k"}, {v :0.5, name: "sw_p"}, {v: 0.5, name:"er_p"}],
                    layout: "circular",
                    forceParameter: {
                        repulsion: 50,
                        gravity: 0.1,
                        edgeLength: 30
                    },
                    mapType: "none",
                    nodeSize: 2,
                    nodeColor: "#409EFF",
                    edgeWith: 1,
                    mapAttr: "deg"
                },
                mapAttrs: ["deg"]
            }
        },
        computed: {
            is_show() {
                if(this.form.networkType === "sf") {
                    return [true, false, false, false];
                }else if(this.form.networkType === "sw") {
                    return [false, true, true, false];
                }else if(this.form.networkType === "random") {
                    return [false, false, false, true];
                }
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