from odoo import fields, models, api

import requests


class Movie(models.Model):
    _name = "movie.movie"

    name = fields.Char(string="name", required=True)
    release_date = fields.Date(string='Release Date', required=True)
    image = fields.Binary(string='Image', widget='image')
    genres = fields.Char(string='Genres')
    description = fields.Text(string='Description')
    price = fields.Float(string='Price', default=0, required=True)

    def fetch_movie_data(self):
        api_url = "https://api.themoviedb.org/3/movie/now_playing?api_key=3a6592f48889a7c2000c7152d60234da"
        response = requests.get(api_url).json()
        vals = []
        for movie in response['results']:
            existing_movie = self.search([('name', '=', movie['title'])])
            if not existing_movie:
                vals.append({
                    'name': movie['title'],
                    'release_date': movie['release_date'],
                    'image': requests.get('https://image.tmdb.org/t/p/w500' + movie['poster_path']).content,
                    'genres': movie['genre_ids'],
                    'description': movie['overview'],
                    'price': 3.00,
                })
            elif existing_movie and existing_movie in response['results']:
                self.search[('name', '=', movie['title'])].update({
                    'name': movie['title'],
                    'release_date': movie['release_date'],
                    'image': requests.get('https://image.tmdb.org/t/p/w500' + movie['poster_path']).content,
                    'genres': movie['genre_ids'],
                    'description': movie['overview'],
                    'price': 3.00,
                })
            else:
                self.search[('name', '=', movie['title'])].unlink()
        self.create(vals)


class Book(models.Model):
    _name = "movie.book"
    _description = "Book a Ticket"

    user_id = fields.Many2one(
        'res.users', string='User', required=True, default=lambda self: self.env.user)
    movie_id = fields.Many2one('movie.movie', string='Movie', required=True)
    ticket_count = fields.Integer(
        string='Ticket Count', required=True, default=1)
    total_price = fields.Float(
        string='Total Price', compute='_compute_total_price', store=True)
    booking_date = fields.Datetime(
        string='Booking Date', required=True, default=fields.Datetime.now)
    date = fields.Date(string='Date', required=True)
    status = fields.Selection(
        [('draft', 'Draft'),
         ('booked', 'Booked'),
         ('cancelled', 'Cancelled')],
        string='Status', required=True, default='draft')

    @api.depends('ticket_count', 'movie_id.price')
    def _compute_total_price(self):
        for booking in self:
            booking.total_price = booking.ticket_count * booking.movie_id.price
