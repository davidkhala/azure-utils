

def fromDataFrame(df, blob_path:str):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    from adlfs import AzureBlobFileSystem

    # 初始化文件系统
    fs = AzureBlobFileSystem(
        account_name="your_account",
        account_key="your_key"
    )

    # DataFrame → Parquet buffer
    table = pa.Table.from_pandas(df)
    buffer = pa.BufferOutputStream()
    pq.write_table(table, buffer)

    # 上传到 Azure
    with fs.open(blob_path, "wb") as f:
        f.write(buffer.getvalue().to_pybytes())
