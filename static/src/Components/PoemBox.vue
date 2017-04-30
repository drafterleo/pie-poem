<template>
    <div class="poem-box w3-card">
        <slot></slot>
    </div>
</template>

<script>
    export default {
    }
</script>

<style>
    .poem-box {
        /*display: inline-block;*/
        width: 400px;
        margin: 5px auto;
        background: #FFF3CD;
    }
</style>