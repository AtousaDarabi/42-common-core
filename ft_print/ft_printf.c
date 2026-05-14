/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/08 15:27:01 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/14 16:36:37 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_print_str(char *str)
{
	if (str == NULL)
		return (write(1, "(null)", 6));
	return (write(1, str, ft_strlen(str)));
}

static	int	ft_print_conversion(char c, va_list arg_list)
{
	int		sum;

	sum = 0;
	if (c == 'c')
		sum = ft_print_char(va_arg(arg_list, int));
	if (c == 's')
		sum = ft_print_str(va_arg(arg_list, char *));
	if (c == 'x' || c == 'X')
		sum = ft_print_hex(va_arg(arg_list, unsigned int), c);
	if (c == 'd' || c == 'i')
		sum = ft_print_number(c, va_arg(arg_list, int), "0123456789");
	if (c == 'u')
		sum = ft_print_number(c, (long)va_arg(arg_list, unsigned int),
				"0123456789");
	if (c == 'p')
		sum = ft_print_pointer(va_arg(arg_list, void *));
	if (c == '%')
		sum = write(1, "%", 1);
	return (sum);
}

int	ft_printf(const char *str, ...)
{
	va_list	ap;
	int		total;
	int		i;

	total = 0;
	i = 0;
	if (str)
	{
		va_start(ap, str);
		while (*(str + i))
		{
			if (*(str + i) == '%')
			{
				total += ft_print_conversion((char)*(str + (i + 1)), ap);
				i++;
			}
			else
			{
				total += write(1, str + i, 1);
			}
			i++;
		}
		va_end(ap);
	}
	return (total);
}

// #include <stdio.h>

// int  main(void)
// {
// 	int     ft_ret;
// 	int     std_ret;

// 	ft_ret = ft_printf("%c\n", 'A');
// 	std_ret = printf("%c\n", 'A');
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %s\n", "Hello World");
// 	std_ret = printf("printf:    %s\n", "Hello World");
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %d\n", 12345);
// 	std_ret = printf("printf:    %d\n", 12345);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %d\n", -12345);
// 	std_ret = printf("printf:    %d\n", -12345);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %d\n", 0);
// 	std_ret = printf("printf:    %d\n", 0);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %i\n", 999);
// 	std_ret = printf("printf:    %i\n", 999);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %u\n", 42);
// 	std_ret = printf("printf:    %u\n", 42);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "�✗");

// 	ft_ret = ft_printf("ft_printf: %u\n", 4294967295U);
// 	std_ret = printf("printf:    %u\n", 4294967295U);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %x\n", 255);
// 	std_ret = printf("printf:    %x\n", 255);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %X\n", 255);
// 	std_ret = printf("printf:    %X\n", 255);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %x\n", 4095);
// 	std_ret = printf("printf:    %x\n", 4095);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %p\n", (void *)"test");
// 	std_ret = printf("printf:    %p\n", (void *)"test");
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %p\n", NULL);
// 	std_ret = printf("printf:    %p\n", NULL);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %%\n");
// 	std_ret = printf("printf:    %%\n");
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %d %s %c %x %%\n", 42, "test", 'X', 255);
// 	std_ret = printf("printf:    %d %s %c %x %%\n", 42, "test", 'X', 255);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %u %x %X %i\n", 100, 255, 255, -99);
// 	std_ret = printf("printf:    %u %x %X %i\n", 100, 255, 255, -99);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %s\n", "");
// 	std_ret = printf("printf:    %s\n", "");
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: Hello World\n");
// 	std_ret = printf("printf:    Hello World\n");
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	ft_ret = ft_printf("ft_printf: %d %d %d\n", 1, 2, 3);
// 	std_ret = printf("printf:    %d %d %d\n", 1, 2, 3);
// 	printf("Return values: ft_printf=%d, printf=%d %s\n\n", ft_ret, std_ret,
// 		ft_ret == std_ret ? "✓" : "✗");

// 	return (0);
// }
