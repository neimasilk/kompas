# get_doc_wiki_id(doc_id)
# get_doc_wiki_zh(doc_id)


# get_doc_kompas (doc_id)
# cari di kompas, buat struktur file kompas seperti wiki


# buat dictionary (doc_id,doc_file_doc_len)


SELECT
    o1.*
FROM
    wiki_id o1
    -- Join all orders with same category and inferior ID
    INNER JOIN wiki_id o2 ON o2.ID <= o1.ID AND o1.judul = o2.judul
GROUP BY
    o1.dokumen,
	o1.judul
HAVING
    SUM(o2.ukuran) < 1000
ORDER BY
    random()
