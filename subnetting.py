import ipaddress


def create_subnets(base_ip, user_requirements):

    # create ipv4 object
    network = ipaddress.ip_network(base_ip)
    subnets = []
    available_network = network

    for num_users in user_requirements:
        # min size is 2 for network ID and Broadcast ID
        # multiply by 2 until can fit required hosts
        subnet_size = 2
        while subnet_size < num_users + 2:
            subnet_size *= 2
        prefix_length = 32 - int(subnet_size.bit_length() - 1)
        print(f"{subnet_size}")
        
        # create subnet object
        new_subnet = next(available_network.subnets(new_prefix=prefix_length))
        subnets.append(new_subnet)

        # exclude subnet from current available network so no overlap
        available_network = list(available_network.address_exclude(new_subnet))[0]

    return subnets


def subnet_info(subnets):
    results = []
    for idx, subnet in enumerate(subnets, 1):
        host_range = f"{subnet.network_address + 1} - {subnet.broadcast_address - 1}"
        wasted = wasted = (
            (subnet.num_addresses - 2)
            - (subnet.num_addresses - len(list(subnet.hosts())))
        ) / subnet.num_addresses

        info = {
            "Subnet Number": idx,
            "Host IP Range": host_range,
            "Broadcast IP": str(subnet.broadcast_address),
            "Wasted Address Percentage": f"{wasted:.2%}",
        }
        results.append(info)
    return results


def find_subnet_for_ip(subnets, dest_ip):
    destination = ipaddress.ip_address(dest_ip)
    for subnet in subnets:
        if destination in subnet:
            return subnet
    return None


def main():
    base_ip = input("Enter the base IP network ")
    num_subnets = int(input("Enter the number of subnets: "))
    user_requirements = []

    for i in range(num_subnets):
        users = int(input(f"Enter the number of required users for subnet {i + 1}: "))
        user_requirements.append(users)

    subnets = create_subnets(base_ip, user_requirements)
    info = subnet_info(subnets)

    for item in info:
        print(item)

    dest_ip = input("Enter a destination IP address to find its subnet: ")
    destination_subnet = find_subnet_for_ip(subnets, dest_ip)
    if destination_subnet:
        print(f"The IP {dest_ip} belongs to subnet: {destination_subnet}")
    else:
        print(f"The IP {dest_ip} does not belong to any subnet.")


main()
