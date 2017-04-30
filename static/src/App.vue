<template>
    <div id="app">
        <div id="search-panel"
             class="w3-container w3-indigo w3-card-4 w3-center">
            <div class="w3-container w3-margin">
                <input id="search-edit"
                       class="w3-input w3-border w3-xlarge"
                       name="search"
                       type="text"
                       v-model="searchText">
                <span id="search-btn"
                      class="material-icons w3-xxlarge"
                      @click="searchPoems()">search</span>
            </div>
        </div>

        <div id="poems-panel">
            <div class="w3-container w3-center">
                <div class="w3-row">
                    <app-poem-box v-for="ipoem in poems" :key="ipoem">
                        <p v-html="ipoem" class="w3-large poem-text"></p>
                    </app-poem-box>
                </div>
            </div>
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
                poemsCount: 10,
                searchText: ''
            }
        },
        components: {
            'app-poem-box': PoemBox
        },
        methods: {
            searchPoems () {
                console.log('searching: ' + this.searchText);
                this.fetchPoems();
                this.poems = [];
                for (let i = 0; i < this.poemsCount; i++) {
                    this.poems.push(this.poem);
                }
            },
            fetchPoems () {
                console.log('fetching: ' + this.searchText);
                let fetchData = {
                    method: 'POST',
                    body: JSON.stringify({
                        words: this.searchText
                    }),
                    headers: new Headers({
                        'Content-Type': "application/x-www-form-urlencoded"
                    })
                };

                fetch('http://127.0.0.1:8081/poems', fetchData)
                    .then(response => response.json())
                    .then(json => console.log(json))
            }
        }
    }
</script>

<style>
    #search-panel {
        position: fixed;
        width: 100%;
        height: 100px;
        z-index: 1000;
    }

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
        color: #ABABAB;
        cursor: pointer;
        width: 0;

        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }

    #search-btn:hover {
        color: #3B3B3B;
    }

    #poems-panel {
        position: relative;
        top: 110px;
        width: 100%;
    }

    .poem-text {
        text-align: left;
        padding: 0 10px;
    }
</style>
