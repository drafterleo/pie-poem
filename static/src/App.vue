<template>
    <div id="app">
        <div class="w3-container w3-indigo w3-card-4 w3-margin w3-center">
            <div class="w3-container w3-margin">
                <input id="search-edit"
                       class="w3-input w3-border w3-xlarge"
                       name="search"
                       type="text">
                <span id="search-btn"
                      class="material-icons w3-xxlarge"
                      @click="searchPoems()">search</span>
            </div>
        </div>

        <div class="w3-container w3-center">
            <app-poem-box v-for="ipoem in poems" :key="ipoem">
                <p v-html="ipoem" class="w3-large poem-text"></p>
            </app-poem-box>
        </div>
    </div>
</template>

<script>
    import PoemBox from './Components/PoemBox.vue'

    export default {
        name: 'app',
        data () {
            return {
                poem: 'полдня пытаюсь поработать<br>' +
                      'полночи не могу заснуть<br>' +
                      'пол утра не могу проснуться<br>' +
                      'и только вечером живу',
                poems: [],
                poemsCount: 10
            }
        },
        components: {
            'app-poem-box': PoemBox
        },
        methods: {
            searchPoems() {
                this.poems = [];
                for (let i = 0; i < this.poemsCount; i++) {
                    this.poems.push(this.poem);
                }
            }
        }
    }
</script>

<style>
    #search-edit {
        display: inline-block;
        width: 70%;
        padding-right: 40px;
    }

    #search-btn {
        position: relative;
        z-index: 1;
        right: 50px;
        top: 10px;
        color: #8B8B8B;
        cursor:pointer;
        width: 0;
    }

    #search-btn:hover {
        color: #3B3B3B;
    }

    .poem-text {
        text-align: left;
        padding: 0 10px;
    }
</style>
