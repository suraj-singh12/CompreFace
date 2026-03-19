## ⚡ Quick Run (After System Restart)

Execute in order:

```bash
# 1. Start Docker
open -a Docker
```

```bash
# 2. Start CompreFace
cd CompreFace
docker compose up -d
```

```bash
# 3. Activate environment
conda activate facerec
```

```bash
# 4. Start backend
cd facerec-system/backend
uvicorn app:app --reload --port 8001
```

```bash
# 5. Start UI
cd ../ui
python3 -m http.server 3000
```

Access:

```text
UI → http://localhost:3000
```
