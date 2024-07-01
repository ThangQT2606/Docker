# Docker
#!/bin/bash
servers=("10.0.2.15")

system_name="Hệ thống A"

output_file="ketqua.txt"

echo "$system_name đang chạy các container sau:" > $output_file

for server in ${servers[@]}; do
    echo "Server $server:" >> $output_file
    ssh dinhthang@$server "docker ps --format '{{.Names}} {{.Image}} {{.Status}}'" >> $output_file
    echo "" >> $output_file
done