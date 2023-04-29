from odoo import fields, api, models


class BookTicketWizard(models.TransientModel):
    _name = "movie.book.ticket.wizard"

    user_id = fields.Many2one(
        'res.users', string='User', required=True, default=lambda self: self.env.user)
    movie_id = fields.Many2one('movie.movie', string='Movie', required=True)
    ticket_count = fields.Integer(
        string='Ticket Count', required=True, default=1)
    total_price = fields.Float(
        string='Total Price', compute='_compute_total_price', store=True)
    booking_date = fields.Datetime(
        string='Booking Date', required=True, default=fields.Datetime.now)
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.today())
    status = fields.Selection(
        [('draft', 'Draft'),
         ('booked', 'Booked'),
         ('cancelled', 'Cancelled')],
        string='Status', required=True, default='draft')

    @api.depends('ticket_count', 'movie_id.price')
    def _compute_total_price(self):
        for booking in self:
            booking.total_price = booking.ticket_count * booking.movie_id.price

    def action_confirm(self):
        data = {
            "form_data": self.read()[0],
        }
        self.env['movie.book'].create({
            'user_id': self.user_id.id,
            'movie_id': self.movie_id.id,
            'ticket_count': self.ticket_count,
            'total_price': self.total_price,
            'booking_date': self.booking_date,
            'date': self.date,
            'status': 'booked'
        })

        self.env.ref('movie.movie_book_receipt').report_action(self, data=data)

    def action_cancel(self):
        self.env['movie.book'].create({
            'user_id': self.user_id.id,
            'movie_id': self.movie_id.id,
            'ticket_count': self.ticket_count,
            'total_price': self.total_price,
            'booking_date': self.booking_date,
            'date': self.date,
            'status': 'cancelled'
        })
