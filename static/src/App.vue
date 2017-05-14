<template>
    <div id="app">
        <app-spinner v-show="showSpinner"></app-spinner>

        <div id="search-panel"
             class="w3-container w3-indigo w3-card-4 w3-center">
            <div class="w3-container w3-margin">
                <input id="search-edit"
                       class="w3-input w3-border w3-xlarge"
                       name="search"
                       type="text"
                       v-model="searchText"
                       @keyup.enter="postPoemsRequest"
                       autofocus>
                <span id="search-btn"
                      class="material-icons w3-xxlarge"
                      @click="postPoemsRequest">search</span>
                <!--<button class="w3-button w3-border w3-transparent w3-large w3-hover-none w3-hover-text-white"-->
                        <!--style="color: #DDD"-->
                        <!--@click="postPoemsRequest">Поиск</button>-->
            </div>
        </div>

        <div id="poems-panel">
            <div class="w3-container w3-center">
                <div class="w3-row">

                    <app-message-box v-if="showStartMessage">
                        <p class="w3-large message-text">
                            Для получения "смыслового эффекта" желательно вводить<br>
                            достаточно редкие, нетипичные слова.<br>
                            Например: аллюзия, лекало, трензель (можно все сразу).
                        </p>
                    </app-message-box>

                    <app-issue-box v-if="showNoPoemsFetched">
                        <p class="w3-large issue-text">Ни одного нормального слова!</p>
                    </app-issue-box>

                    <app-issue-box v-if="showError">
                        <p class="w3-large issue-text">Ошибка сервера!</p>
                    </app-issue-box>

                    <app-poem-box v-for="ipoem in poems" :key="ipoem" v-if="showFetchedPoems">
                        <p v-html="ipoem" class="w3-large poem-text"></p>
                    </app-poem-box>

                </div>
            </div>
        </div>

    </div>
</template>

<script>
    import MessageBox from './Components/MessageBox.vue'
    import PoemBox from './Components/PoemBox.vue'
    import IssueBox from './Components/IssueBox.vue'
    import Spinner from './Components/Spinner.vue'

    export default {
        name: 'app',
        components: {
            'app-poem-box'   : PoemBox,
            'app-issue-box'  : IssueBox,
            'app-message-box': MessageBox,
            'app-spinner'    : Spinner
        },
        data () {
            return {
                poem: 'полдня пытаюсь поработать<br>' +
                      'полночи не могу заснуть<br>' +
                      'пол утра не могу проснуться<br>' +
                      'и только вечером живу',
                poems: [],
                poemsCount: 10,
                searchText: '',
                fetchStarted: false,
                showStartMessage: true,
                showSpinner: false,
                showFetchedPoems: false,
                showNoPoemsFetched: false,
                showError: false,
                errorText: ''
            }
        },
        watch: {
//            showSpinner: function (val) {
//                console.log('showSpinner = ' + val);
//            }
        },
        methods: {
            genPoems () {
                this.poems = [];
                for (let i = 0; i < this.poemsCount; i++) {
                    this.poems.push(this.poem);
                }
            },
            fetchPoems () {
                if (this.fetchStarted) {
                    return;
                }

                let fetchData = {
                    method: 'POST',
                    body: JSON.stringify({
                        words: this.searchText.replace(/,|\.|!|\?|;|"|@|#|%|&|\*|\\|\/|:|\+/gi, ' ').trim()
                    }),
                    headers: new Headers({
                        'Content-Type': "application/x-www-form-urlencoded"
                    })
                };

                this.showSpinner = true;
                this.showNoPoemsFetched = false;
                this.showError = false;

                let poemsUrl = '/poems';
                //let poemsUrl = 'http://192.168.135.135:8085/poems';
                //let poemsUrl = 'http://127.0.0.1:8085/poems';
//
//                let fetchData = JSON.stringify({
//                    words: this.searchText.replace(/,|\.|!|\?|;|"|@|#|%|&|\*|\\|\/|:|\+/gi, ' ').trim()
//                });
//
//                console.log(fetchData)

                this.fetchStarted = true;
                fetch(poemsUrl, fetchData)
                    .then(response => response.json())
                    .then(data => {
                        window.scrollTo(0, 0);
                        this.showSpinner = false;
                        this.showStartMessage = false;
                        this.poems = data;
                        if (this.poems.length > 0) {
                            this.showFetchedPoems = true;
                        } else {
                            this.showFetchedPoems = false;
                            this.showNoPoemsFetched = true;
                        }
                        this.fetchStarted = false;
                    })
                    .catch(error => {
                        this.errorText = error.text;
                        window.scrollTo(0, 0);
                        this.showStartMessage = false;
                        this.showSpinner = false;
                        this.showError = true;
                        this.showFetchedPoems = false;
                        this.fetchStarted = false;
                    });
            },
            postPoemsRequest() {
                let postData = JSON.stringify({
                    words: this.searchText.replace(/,|\.|!|\?|;|"|@|#|%|&|\*|\\|\/|:|\+/gi, ' ').trim()
                });

                this.showSpinner = true;
                this.showNoPoemsFetched = false;
                this.showError = false;

                let poemsUrl = '/poems';
                //let poemsUrl = 'http://192.168.135.135:8085/poems';
                //let poemsUrl = 'http://127.0.0.1:8085/poems';

                let xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function(vue) {
                    if (xhr.readyState != 4)
                        return;
                    if (xhr.status == 200) {
                         window.scrollTo(0, 0);
                        vue.showSpinner = false;
                        vue.showStartMessage = false;
                        vue.poems = JSON.parse(xhr.responseText);
                        if (vue.poems.length > 0) {
                            vue.showFetchedPoems = true;
                        } else {
                            vue.showFetchedPoems = false;
                            vue.showNoPoemsFetched = true;
                        }
                        vue.fetchStarted = false;
                    } else {
                        vue.errorText = xhr.statusText;
                        window.scrollTo(0, 0);vue.showStartMessage = false;
                        vue.showSpinner = false;
                        vue.showError = true;
                        vue.showFetchedPoems = false;
                        vue.fetchStarted = false;
                    }
                }.bind(xhr, this); // bind Vue instance to xhr.onreadystatechange

                xhr.open("POST", poemsUrl, true);
                xhr.setRequestHeader("Content-type", "application/json");
                xhr.send(postData);
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

    .message-text, .issue-text {
        text-align: center;
        padding: 0 10px;
    }

</style>
