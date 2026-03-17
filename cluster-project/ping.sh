# ping all nodes in the cluster

success=true

# || means "or" - it runs the right side only if the left side fails

echo "head"
ping -c 1 10.0.1.100 || success=false
echo

# ping all workers
for i in {1..4}; do
	echo "worker 10$i"
	ping -c 1 10.0.1.10$i || sucess=false
	echo
done

if $success; then
	echo "All nodes reachable!"
else
	echo "One or more nodes failed"
fi


