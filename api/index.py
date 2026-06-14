import os
import sys

# Force the Python runtime execution environment to recognize the root repository directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Now Python can safely locate your modular engines without crashing
from stormcore_si import ComplianceShield, TargetTracker
from stormcore_si.platform_poster import PlatformPoster
from stormcore_si.payment_gateways import PaymentGatewayCoordinator

app = FastAPI()
# ... (leave the rest of your index.py file exactly as it was)
