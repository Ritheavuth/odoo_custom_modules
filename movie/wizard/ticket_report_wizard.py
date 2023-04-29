from odoo import fields, models, api


class TicketReportWizard(models.TransientModel):
    _name = "ticket.report.wizard"

    movie_id = fields.Many2one('movie.movie', required="True")
    date_from = fields.Date(string="Date From", required="True")
    date_to = fields.Datetime(string="Date To", required="True")

    def action_print_report(self):
        tickets = self.env['movie.book'].search_read([
            ("movie_id.id", "=", self.movie_id.id),
            ("booking_date", "<=", self.date_to),
            ("status", "=", "booked")
        ])
        print("Tickets filtered: ", tickets)
        total_tickets = sum(ticket['ticket_count'] for ticket in tickets)
        total_price = sum(ticket['total_price'] for ticket in tickets)
        print(total_tickets, total_price)
        data = {
            "form_data": self.read()[0],
            "total_tickets": total_tickets,
            "total_price": total_price
        }

        return self.env.ref('movie.movie_book_ticket_report').report_action(self, data=data)
