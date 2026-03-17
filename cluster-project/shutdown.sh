#!/bin/bash
for i in {100..104}; do
	ssh luis@10.0.1.$i "sudo shutdown now"
done
