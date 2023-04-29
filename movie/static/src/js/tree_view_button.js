odoo.define('movie.tree_view_button', function(require) {
    "use strict"
    var rpc = require('web.rpc');
    var ListController = require('web.ListController')

    ListController.include({
        renderButtons: function($node) {
            this._super.apply(this, arguments);
            var self = this;
            if (this.$buttons) {
                $(this.$buttons).find('.oe_new_custom_button').on('click', function() {
                    rpc.query({
                        model: 'movie.movie',
                        method: 'fetch_movie_data',
                        args: [],
                    }).then(function(res) {
                        console.log(res)
                        self.reload()
                    })
                })
            }
        }
    })
})