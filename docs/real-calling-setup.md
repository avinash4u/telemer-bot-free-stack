# 📞 Real Calling Setup Guide

## 🎯 Recommended: FreeVoIPDeal

### 📋 Quick Setup (15 minutes)

#### Step 1: Create FreeVoIPDeal Account
```bash
# 1. Go to https://www.freevoipdeal.com/
# 2. Click "Sign Up" 
# 3. Fill in details:
#    - Email: your.email@example.com
#    - Password: your_password
#    - Country: United States
# 4. Verify email
# 5. Login to dashboard
```

#### Step 2: Get SIP Credentials
```bash
# In FreeVoIPDeal dashboard:
# 1. Go to "SIP Settings" or "Account Settings"
# 2. Note your credentials:
#    - SIP Username: your_username
#    - SIP Password: your_password
#    - SIP Server: sip.freevoipdeal.com
#    - SIP Port: 5060
```

#### Step 3: Update Configuration
```bash
# Edit FreeSWITCH configuration:
vim /configs/freeswitch/autoload_configs/sip_profiles/external.xml

# Replace placeholders:
YOUR_FREEVOIPDEAL_USERNAME → your_actual_username
YOUR_FREEVOIPDEAL_PASSWORD → your_actual_password
```

#### Step 4: Restart Services
```bash
# Restart FreeSWITCH
docker restart telemer-bot-free-stack-freeswitch-1

# Restart Orchestrator
docker restart telemer-bot-free-stack-orchestrator-1
```

#### Step 5: Test Registration
```bash
# Check if FreeVoIPDeal gateway is registered
docker exec telemer-bot-free-stack-freeswitch-1 fs_cli -p ClueCon -x "sofia status gateway freevoipdeal_trunk"

# Should show: "REGISTERED" status
```

#### Step 6: Make Test Call
```bash
# Test outbound call to your phone
curl -X POST http://localhost:8000/calls/outbound \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+15551234567",
    "caller_id": "TeleMER",
    "proposal_id": "TEST_CALL_001"
  }'
```

## 📊 Expected Results

### ✅ Success Indicators:
- **Gateway Status**: REGISTERED
- **Call Initiation**: +OK response
- **Phone Rings**: Your phone should ring
- **Bot Answers**: TeleMER bot should respond

### 📞 Call Flow:
```
You dial → FreeVoIPDeal → FreeSWITCH → TeleMER Bot → AI Processing
```

## 🔧 Troubleshooting

### ❌ Gateway Not Registering:
```bash
# Check FreeSWITCH logs
docker logs telemer-bot-free-stack-freeswitch-1 | grep -i register

# Verify credentials in config
grep -A 10 "freevoipdeal_trunk" /configs/freeswitch/autoload_configs/sip_profiles/external.xml
```

### ❌ Call Not Connecting:
```bash
# Check SIP registration
docker exec telemer-bot-free-stack-freeswitch-1 fs_cli -p ClueCon -x "sofia status"

# Test manual call
docker exec telemer-bot-free-stack-freeswitch-1 fs_cli -p ClueCon -x "originate sofia/gateway/freevoipdeal_trunk/15551234567 &echo(test)"
```

### ❌ Audio Issues:
```bash
# Check RTP ports
docker ps | grep freeswitch

# Verify firewall allows RTP (16384-16464)
```

## 💰 Cost Analysis

### FreeVoIPDeal Rates (2024):
- **US Calls**: $0.009/minute
- **UK Calls**: $0.012/minute  
- **India Calls**: $0.015/minute

### Example Costs:
```
100 calls/day × 3 minutes × $0.009 = $2.70/day
100 calls/day × 30 days = $81/month
```

## 🚀 Production Deployment

### For Production Use:
1. **Add credits** to FreeVoIPDeal account
2. **Get DID number** for inbound calls
3. **Configure IVR** for call routing
4. **Monitor usage** and costs
5. **Set up alerts** for low balance

### Scaling Considerations:
- **Multiple gateways** for redundancy
- **Load balancing** across providers
- **Cost optimization** with routing rules
- **Quality monitoring** and analytics

## 🎯 Next Steps

### After Setup Works:
1. **Test end-to-end flow**
2. **Configure DID numbers**
3. **Set up monitoring**
4. **Deploy to production**
5. **Monitor call quality**

### Advanced Features:
- **Call recording** (MinIO storage)
- **Call analytics** (database insights)
- **Quality monitoring** (sentiment tracking)
- **Automated reporting** (compliance)

---

**🎉 Your TeleMER bot will be making real calls in 15 minutes!**
