# Generate SSH key if not already present
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519

# Copy to all workers
for i in {101..104}; do
  ssh-copy-id luis@10.0.1.$i
done

# Test
for i in {101..104}; do
  ssh luis@10.0.1.$i "echo Worker $i responding"
done

