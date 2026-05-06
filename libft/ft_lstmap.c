/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/30 15:04:28 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:53:33 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
// #include <ctype.h>

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*new_list;
	t_list	*new_node;
	void	*content;

	if (!lst || !f || !del)
		return (NULL);
	new_list = NULL;
	while (lst)
	{
		content = f(lst->content);
		new_node = ft_lstnew(content);
		if (!new_node)
		{
			del(content);
			ft_lstclear(&new_list, del);
			return (NULL);
		}
		ft_lstadd_back(&new_list, new_node);
		lst = lst->next;
	}
	return (new_list);
}

// void	*make_uppercase(void *content)
// {
// 	char	*str;
// 	int		i;

// 	str = ft_strdup((char *)content);
// 	i = 0;
// 	if (!str)
// 		return (NULL);
// 	while (str[i])
// 	{
// 		str[i] = toupper(str[i]);
// 		i++;
// 	}
// 	return (str);
// }

// void	del_content(void *content)
// {
// 	free(content);
// }

// void	ft_print(t_list *tmp)
// {
// 	while (tmp)
// 	{
// 		printf("- %s\n", (char *)tmp->content);
// 		tmp = tmp->next;
// 	}
// }

// int	main(void)
// {
// 	t_list	*list_a;
// 	t_list	*list_b;
// 	t_list	*tmp;

// 	list_a = NULL;
// 	list_b = NULL;
// 	ft_lstadd_back(&list_a, ft_lstnew(ft_strdup("hello")));
// 	ft_lstadd_back(&list_a, ft_lstnew(ft_strdup("world")));
// 	ft_lstadd_back(&list_a, ft_lstnew(ft_strdup("!!!")));
// 	list_b = ft_lstmap(list_a, make_uppercase, del_content);
// 	printf("Original List A:\n");
// 	tmp = list_a;
// 	ft_print(tmp);
// 	printf("\nMapped List B (Uppercase):\n");
// 	tmp = list_b;
// 	ft_print(tmp);
// 	ft_lstclear(&list_a, del_content);
// 	ft_lstclear(&list_b, del_content);
// 	return (0);
// }
