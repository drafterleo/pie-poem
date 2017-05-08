<template>
    <div class="poem-box w3-card">
        <slot></slot>
    </div>
</template>

<script>
    export default {
    }
</script>

<style scoped>
    .poem-box {
        /*display: inline-block;*/
        width: 450px;
        margin: 5px auto;
        background: #FFF3CD;
    }
</style>