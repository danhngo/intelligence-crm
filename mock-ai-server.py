#!/usr/bin/env python3
"""
Simple mock AI orchestration server for testing frontend integration
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import uuid
import datetime
import urllib.parse


class MockAIHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        
        if self.path == '/api/v1/models/':
            # Mock models list
            models = [
                {
                    "id": str(uuid.uuid4()),
                    "name": "Lead Scoring Model",
                    "type": "classification",
                    "status": "active",
                    "accuracy": 0.89,
                    "version": "v1.2",
                    "created_at": datetime.datetime.utcnow().isoformat(),
                    "last_trained": datetime.datetime.utcnow().isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Customer Segmentation",
                    "type": "clustering",
                    "status": "training",
                    "accuracy": 0.76,
                    "version": "v2.1",
                    "created_at": datetime.datetime.utcnow().isoformat(),
                    "last_trained": datetime.datetime.utcnow().isoformat()
                }
            ]
            self.wfile.write(json.dumps(models).encode())
            
        elif self.path == '/api/v1/predictions/':
            # Mock predictions list
            predictions = [
                {
                    "job_id": str(uuid.uuid4()),
                    "status": "completed",
                    "model_id": str(uuid.uuid4()),
                    "total_items": 100,
                    "completed_items": 100,
                    "failed_items": 0,
                    "progress": 100.0,
                    "created_at": datetime.datetime.utcnow().isoformat(),
                    "completed_at": datetime.datetime.utcnow().isoformat()
                }
            ]
            self.wfile.write(json.dumps(predictions).encode())
            
        elif self.path.startswith('/api/v1/training/'):
            if self.path == '/api/v1/training/':
                # Mock training jobs list
                jobs = [
                    {
                        "job_id": str(uuid.uuid4()),
                        "model_name": "Customer Churn Predictor",
                        "algorithm": "random_forest",
                        "status": "running",
                        "progress": 67.5,
                        "metrics": {
                            "accuracy": 0.84,
                            "loss": 0.23,
                            "validation_accuracy": 0.81,
                            "validation_loss": 0.28
                        },
                        "created_at": datetime.datetime.utcnow().isoformat(),
                        "estimated_completion": (datetime.datetime.utcnow() + datetime.timedelta(minutes=15)).isoformat()
                    }
                ]
                self.wfile.write(json.dumps(jobs).encode())
            
        elif self.path == '/api/v1/workflows/':
            # Mock workflows list
            workflows = [
                {
                    "id": str(uuid.uuid4()),
                    "name": "Lead Scoring Pipeline",
                    "description": "Automated lead scoring and routing workflow",
                    "status": "active",
                    "type": "ml_pipeline",
                    "steps": 5,
                    "success_rate": 0.94,
                    "created_at": datetime.datetime.utcnow().isoformat(),
                    "last_run": datetime.datetime.utcnow().isoformat()
                }
            ]
            self.wfile.write(json.dumps(workflows).encode())
            
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        self._set_headers()
        
        if self.path == '/api/v1/models/':
            # Create new model
            model = {
                "id": str(uuid.uuid4()),
                "name": "New AI Model",
                "type": "classification",
                "status": "training",
                "created_at": datetime.datetime.utcnow().isoformat()
            }
            self.wfile.write(json.dumps(model).encode())
            
        elif self.path == '/api/v1/predictions/batch':
            # Start batch prediction
            job = {
                "job_id": str(uuid.uuid4()),
                "status": "queued",
                "message": "Batch prediction job started",
                "created_at": datetime.datetime.utcnow().isoformat()
            }
            self.wfile.write(json.dumps(job).encode())
            
        elif self.path == '/api/v1/training/':
            # Start training job
            job = {
                "job_id": str(uuid.uuid4()),
                "status": "queued",
                "message": "Training job started",
                "created_at": datetime.datetime.utcnow().isoformat()
            }
            self.wfile.write(json.dumps(job).encode())
            
        else:
            self.send_error(404)


def run_server():
    server_address = ('', 8005)
    httpd = HTTPServer(server_address, MockAIHandler)
    print(f"Mock AI Orchestration Server running on port 8005...")
    print("Available endpoints:")
    print("  GET /api/v1/models/")
    print("  POST /api/v1/models/")
    print("  GET /api/v1/predictions/")
    print("  POST /api/v1/predictions/batch")
    print("  GET /api/v1/training/")
    print("  POST /api/v1/training/")
    print("  GET /api/v1/workflows/")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()