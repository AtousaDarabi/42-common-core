/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_helper.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/12 15:44:01 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/12 22:44:00 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_char(char c)
{
	return (write(1, &c, 1));
}

int	ft_print_hex(unsigned long nbr, char c)
{
	if (c == 'X')
		return (ft_print_hex_helper(nbr, "0123456789ABCDEF"));
	return (ft_print_hex_helper(nbr, "0123456789abcdef"));
}

int	ft_print_hex_helper(unsigned long nbr, char *arr)
{
	int	total;

	if (nbr / 16 == 0)
		total = write(1, &(arr[nbr % 16]), 1);
	else
	{
		total = ft_print_hex_helper(nbr / 16, arr);
		total += write(1, &(arr[nbr % 16]), 1);
	}
	return (total);
}

int	ft_print_number(char c, long l, char *arr)
{
	long	nbr;
	int		total;

	total = 0;
	if (c == 'u')
		nbr = (unsigned long)l;
	else
		nbr = (int)l;
	if (nbr < 0)
	{
		total += write(1, '-', 1);
		nbr = nbr * -1;
	}
	if (nbr / 10 == 0)
		total += write(1, &arr[nbr % 10], 1);
	else
	{
		total += ft_print_number(c, nbr / 10, arr);
		total += write(1, &arr[nbr % 10], 1);
	}
	return (total);
}

int	ft_print_pointer(void *ptr)
{
	int				total;
	unsigned long	ptrnbr;
	char			*str;

	ptrnbr = (unsigned long)ptr;
	if (ptrnbr == 0)
		total += write(1, "(nil)", 1);
	else
	{
		total += write(1, "0x", 2);
		total += ft_print_hex_helper(ptrnbr, "0123456789abcdef");
	}
	return (total);
}
