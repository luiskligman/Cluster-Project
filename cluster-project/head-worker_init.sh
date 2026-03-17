for i in {101..104}; do
  ssh luis@10.0.1.$i "mkdir -p ~/files/"
  scp ~/files/init.sh luis@10.0.1.$i:~/files/
  ssh luis@10.0.1.$i "bash ~/files/init.sh"
done
