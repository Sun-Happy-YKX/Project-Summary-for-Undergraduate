for /L %%I in (1, 1, 200) do (
python Model.py
echo %%I)