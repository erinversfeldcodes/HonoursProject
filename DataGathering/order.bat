@echo off
for /l %%N in (1 1 50) do (
    set "participant_file="
    set /p participant_file="Participant (filename): "
    python create_order.py %participant_file%
)
endlocal

