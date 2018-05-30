inq="/usr/share/owlh/in_queue"
outq="/usr/share/owlh/out_queue"
while :
do
  for f in `ls "$inq"/*.pcap`; do
    sudo tcpreplay -i owlh -t -l 1 "$f"
    mv "$f" "$outq"/
  done
  sleep 10
done
