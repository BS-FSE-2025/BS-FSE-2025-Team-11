import unittest

class TestRequestStatusTracking(unittest.TestCase):

#Test access to order status page
    def test_access_request_status_page(self):
        response = self.client.get('/request-status')
        self.assertEqual(response.status_code, 200)
#Test display of order list
    def test_display_request_list(self):
        response = self.client.get('/request-status')
        requests = response.json()
        self.assertGreater(len(requests), 0)
#Test display order status
    def test_display_request_status(self):
        response = self.client.get('/request-status')
        requests = response.json()
        for request in requests:
            self.assertIn(request['status'], ['pending', 'approved', 'rejected'])
#Test display of available actions based on request status
    def test_available_actions_by_status(self):
        response = self.client.get('/request-status')
        requests = response.json()
        for request in requests:
            if request['status'] == 'rejected':
                self.assertIn('appeal', request['actions'])
            elif request['status'] == 'approved':
                self.assertIn('view', request['actions'])
            elif request['status'] == 'pending':
                self.assertIn('cancel', request['actions'])
#Page Load Performance Test
    def test_page_load_performance(self):
        import time
        start_time = time.time()
        self.client.get('/request-status')
        load_time = time.time() - start_time
        self.assertLess(load_time, 3)
# Security and Access Control Testing
    def test_security_access_control(self):
        self.client.logout()
        response = self.client.get('/request-status')
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
