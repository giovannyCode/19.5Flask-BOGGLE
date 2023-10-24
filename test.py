from unittest import TestCase
from app import app
from flask import session 
from boggle import Boggle
import json


class FlaskTests(TestCase):

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Boggle</h1>', html)

    def test_validate_word(self):
        with app.test_client() as client:
            client.get("/")
            resp = client.post('validateWord',data =json.dumps(dict(word="bjfbdsfkjbdskjbf")),content_type ='application/json') 
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('not-word', html)

    def test_validate_word2(self):
        with app.test_client() as client:
            client.get("/")
            resp = client.post('validateWord',data =json.dumps(dict(word="Aaronitic")),content_type ='application/json') 
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('not-on-board', html)

    def test_validate_word3(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['W', 'A', 'T', 'E', 'R'], ['T', 'D', 'A', 'P', 'J'], ['Q', 'X', 'V', 'K', 'Q'], ['J', 'F', 'H', 'L', 'N'], ['K', 'Q', 'G', 'L', 'T']]
            resp = client.post('validateWord',data =json.dumps(dict(word="water")),content_type ='application/json') 
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('ok', html)
    
    def test_statistics(self):
        with app.test_client() as client:
            resp = client.post('statistics',data =json.dumps(dict(currentScore="0")),content_type ='application/json') 
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['timesPlayed'],0)
            self.assertIn('maxScore', html)
            self.assertIn('0', html)
            resp = client.post('statistics',data =json.dumps(dict(currentScore="5")),content_type ='application/json')
            html2 = resp.get_data(as_text=True)
            self.assertIn('"maxScore": 5', html2)
            self.assertEqual(session['timesPlayed'],1)
