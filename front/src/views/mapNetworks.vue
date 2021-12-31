<template>
    <div class="container">
        <div ref="mainsvg" class="mainsvg">

        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import * as echarts from "echarts";
    export default {
        name: "mapNetworks",
        mounted() {
            this.charts = echarts.init(this.$refs.mainsvg);

            axios.get(this.mapDataUrl).then(res => {
                this.mapData = res.data.data;
                console.log(this.mapData.links);
                console.log(this.mapData.nodes);
                const options = {
                    series: [{
                        type: "graph",
                        data: this.mapData.nodes,
                        links: this.mapData.links,
                        layout: "none"
                    }]
                }



                this.charts.setOption(options);
            })


        },
        data() {
            return {
                mapDataUrl: "http://10.154.51.137:8000/nets/map/",
                mapData: null
            }
        }
    }
</script>

<style scoped>

    .container{
        width: 100%;
        height: 100%;
    }

    .mainsvg{
        height: 100%;
        width: 100%;
    }

</style>