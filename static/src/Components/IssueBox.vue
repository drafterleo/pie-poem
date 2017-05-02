<template>
    <div class="issue-box w3-card">
        <slot></slot>
    </div>
</template>

<script>
    export default {
    }
</script>

<style scoped>
    .issue-box {
        /*display: inline-block;*/
        width: 400px;
        margin: 5px auto;
        background: #ffb8ad;
    }
</style>