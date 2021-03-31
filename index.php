<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Bottlo Run</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="../3rd-party-js/d3-v5.12.0/d3.js"></script>
        <script src="../3rd-party-js/vue-2.6.10/vue.js"></script> 
    </head>
    <style>
        body {
            background-color: #378aad;
	        font-family: Arial, Helvetica, sans-serif;
	        font-size: calc(18px + (19 - 14) * ((100vw - 300px) / (1600 - 300)));
            color: #fff;   
	    }
        #app{
            width:50%; 
            margin:0% 25% 0%;	
        }
        span{
            right : 25%;
            width : 50%;
            height : auto;
            position: absolute;
            z-index: -1;
        }
        .refresh{
            margin-left: -95%;
            width: 2vw;
            height: 2vw;
        }
        .refresh:hover{
            width: 2.3vw;
            height: 2.3vw;
        }

        .table{
            width:50%;
            margin: 15% 0%;
            position: absolute;
        }
        table{
            width:100%;
            border-collapse: collapse;
            background-color: rgba(255,255,255,0.3);
        }
        th, td{ border: 1px solid rgba(255,255,255,0.3); }
        th{ background-color: rgba(83,140,184,0.3);}
        #loader{
            border: 1em solid #57b4eb;
            border-top: 1em solid rgba(87,180,235,0.6);
            border-radius: 50%;
            width: 10em;
            height: 10em;
            animation: spin 2s linear infinite;
            position: fixed;
            top:45%;
            right: 45%;
            z-index: 1000000 !important;
        }
        @keyframes spin{
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @media only screen and (max-width: 768px) {
            #app{
                width:100%; 
                margin:0% 0%;	
            }
            span{
                left: 5%;
                width: 90%;
            }
            .refresh{
                width: 5vw;
                height: 5vw;
            }
            .refresh:hover{
                width: 5.3vw;
                height: 5.3vw;
            }
            .table{
                width: 90%;
                margin: 20% 2.5%;
            }
            #loader{
                width: 10rem;
                height: 10rem;
                top:25%;
                right: 25%;
            }
        }

    </style>
    <body> 
        <center id="app">
            <span>
                 <object type="image/svg+xml" data="images/bottlo_run_logo.svg"></object>
            </span>
            <div class="table">
                <object v-on:click="getprices()" class="refresh" type="image/svg+xml" data="images/refresh.svg"></object>
                <table>
                      <tr>
                          <th>Store</th>
                          <th>Corona</th>
                          <th>Summer</th>
                      </tr>
                      <tr v-for="(store, idx) in prices">
                          <td>{{ idx }} </td>
                          <td>${{ store['corona'] }}</td>
                          <td>${{ store['summer'] }}</td>
                     </tr>
                 </table>
             </div>
             <div id="loader" v-bind:style="{display:loaderDisplay}"></div>
        </center>
    </body>
    <script>
    var app = new Vue({
        el: '#app',
        data: {
            loaderCounter: 1,    
            loaderDisplay: 'block',
            prices: []

        },
        created() {
            app = this;	
            this.getprices();
        },
        watch: {
             loaderCounter: function(val){
                 if(app.loaderCounter == 0){
                    app.loaderDisplay = 'none';     
                 }else{
                    app.loaderDisplay = 'block';     
                 }
             }
        },
        methods: {
            getprices: function(){ 
                app.loaderShow = true;
                d3.json("bottlo_run.py").then(function(data){
                    app.prices = data;
                    app.loaderCounter = app.loaderCounter - 1;
                },function(error){alert("AJAX fetch of bottlo_run.py " + error.responseURL + " failed!");});
            }
        }    
    })
    </script>
</html>
