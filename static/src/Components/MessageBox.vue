<template>
    <div class="message-box w3-card w3-pale-green">
        <slot></slot>
    </div>
</template>

<script>
    export default {
    }
</script>

<style scoped>
    .message-box {
        width: 600px;
        margin: 5px auto;
    }
</style>