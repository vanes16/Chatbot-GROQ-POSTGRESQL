# GROQ-POSTGRESQL-PINECONE-Chatbot

1. User Input ├─> Pengguna mengetik pertanyaan ke chatbot ↓

2. Normalize Input menjadi huruf kecil dan menghilangkan symbol

3. Cek di PostgreSQL (Database Utama) ├ (Vector Embedding) ├─> Cari pertanyaan serupa menggunakan vektor Embedding sentence-transformers (dimensi 1024)  atau yang lain ├─> Jika ditemukan pertanyaan serupa dengan relevansi 0.8 → Ambil & kirim jawaban dari DB ✅ 
Jika relevansi dibawah 0.8 ├─> Berikan ke Groq sebagai jawaban konteks ✅ 

4. Output ke User ├─> Jawaban dikirim kembali ke pengguna 

Database Input :
- Input question dan answer
- Question akan di ubah menjadi vector dengan dimensi 1024

❌ Tidak menggunakan model lokal 
❌ Tidak membuat model sendiri
❌ Tidak menggunakan Pinecone
❌ Tidak melakukan summarization input db + input groq -> summarize
❌ Tidak menggunakan conversation memory. Contoh input pertama apa itu chatbot. Input kedua jelaskan lebih detail konteks sebelumnya.
❌ Bukan AI Agent. contoh input beli tiket untuk besok -> cari harga untuk besok, bandingkan, booking.

❌ Hybrid search sudah ada di code belum dicoba untuk testing implement.
