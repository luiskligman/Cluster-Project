# Test SSH to all workers 
for i in {101..104}; do
  ssh luis@10.0.1.$i "echo Worker $i: \$(hostname) is ready"
done

# Test Redis from all workers
for i in {101..104}; do
  ssh luis@10.0.1.$i "redis-cli -h 10.0.1.100 ping"
done

# Check Docker is installed on all nodes
for i in {101..104}; do
  ssh luis@10.0.1.$i "docker --version"
done
docker --version  # check on head also
